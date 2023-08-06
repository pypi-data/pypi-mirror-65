# -*- coding: utf-8 -*-
from __future__ import absolute_import

from xml.etree.ElementTree import ParseError

from six.moves.urllib.parse import urljoin
from datetime import datetime, date
import time
import logging
import json
import xml.etree.ElementTree as ET

from fei_ws.utils import normalize_name
from .base import FEIWSBaseClient
from fei_ws import config
from fei_ws.clients import errors as fei_errors
import requests

logger = logging.getLogger('fei-ws.client')


class FEIWSClient(FEIWSBaseClient):
    def __init__(self, username=None, password=None):
        logger.info('initialize FEI WS Client')
        super(FEIWSClient, self).__init__((1, 2), username, password)

    def find_athlete(self, fei_ids=None, family_name=None, first_name=None,
                     gender_code=None, competing_for=None):
        """
        Find athletes based on a certain search criteria.
        :param fei_ids: A tuple of Athlete FEI IDs you want to search for.
        :param family_name: The athlete's family name. Use % to create a `contain` query
        :param first_name: The athlete's first name. User % to create a `contain` query
        :param gender_code: The athlete gender(None=All, M=Male, F=Female)
        :param competing_for: The NOC code of the athlete's country he is competing for
        :return: An array of Athlete objects.
        """

        fei_ids_array = None
        if fei_ids:
            fei_ids_array = self._ows_factory.ArrayOfString(string=fei_ids)
        response = self.get_organizer_data('findAthlete',
            FEIIDs=fei_ids_array, FamilyName=family_name, FirstName=first_name,
            GenderCode=gender_code, CompetingFor=competing_for)
        results = response.AthleteOC if hasattr(response, 'AthleteOC') else []
        if self.normalize:
            NORMALIZE_RANKING_FIELDS = ('AthleteFamilyName', 'HorseName')
            for athlete in results:
                athlete.FamilyName = self._normalize_name(athlete.FamilyName)
                if hasattr(athlete, 'Rankings') and getattr(athlete.Rankings, 'RankingOC', None):
                    for ranking in athlete.Rankings.RankingOC:
                        ranking.AthleteFamilyName = self._normalize_name(getattr(ranking, 'AthleteFamilyName', None))
                        ranking.HorseName = self._normalize_name(getattr(ranking, 'HorseName', None), roman_nummerals=True)
        return results

    def find_official(self, any_id=None, any_name=None, person_gender=None,
                     admin_nf=None, person_status=None, official_function=None,
                     official_function_discipline=None):
        """
        Find officials based on a certain search criteria.
        :param any_id: Return officials having this ID, licence nr, or vet delegat nr.
        :param any_name: Return officials having this family name, first name, nick name.
            use % to make a `contain` search.
        :param person_gender: Return officials with this gender (None=All, M=Male, F=Female)
        :param admin_nf: Return official that are member of the administrative NF
        :param person_status: Return the official having this status:
                10: Search for all competitors
                1: Search only for active competitors
                0: Search only for inactive competitors
                2: Search only for pending competitors
                3: Search only for cancelled competitors
                9: Search only for suspended competitors.
        :param official_function: Search for officials with specified function
        :param official_function_discipline: Return officials having the specified official
                function for this discipline.
        :return: An array of PersonOfficialOC objects
        """
        response = self.get_organizer_data('findOfficial',
            AnyID=any_id, AnyName=any_name, PersonGender=person_gender, AdminNF=admin_nf,
            PersonStatus=person_status, OfficialFunction=official_function,
            OfficialFunctionDiscipline=official_function_discipline)
        results = response.PersonOfficialOC if hasattr(response, 'PersonOfficialOC') else []
        if self.normalize:
            for official in results:
                official.FamilyName = self._normalize_name(getattr(official, 'FamilyName', None))
        return results

    def find_horse(self, fei_ids=None, name=None, sex_code=None, is_pony=None,
                   athlete_fei_id=None):
        """
        Find horses based on a certain search criteria.
        :param fei_ids: A tuple of Horse FEI IDs you want to search for.
        :param name: The name of the horse. Use % to create a contain query
        :param sex_code: The sex code of the horse (None=All, F=Mare, G=Gelding,
                S=Stallion, M=Male Unknown, U=Unknown).
        :param is_pony: Boolean indicating to search for only ponies.
        :param athlete_fei_id: Search for horses associated with this Athlete.
        :return: A list of Horse objects.
        """
        fei_ids_array = None
        if fei_ids:
            fei_ids_array = self._ows_factory.ArrayOfString(string=fei_ids)
        response = self.get_organizer_data('findHorse',
            FEIIDs=fei_ids_array, Name=name, SexCode=sex_code, IsPony=is_pony,
            AthleteFEIID=athlete_fei_id)
        results = response.HorseOC if hasattr(response, 'HorseOC') else []
        if self.normalize:
            NORMALIZE_FIELDS = ('BirthName', 'CurrentName', 'CommercialName', 'CompleteName', 'ShortenName',
                                'HorseSireName', 'HorseDamName', 'HorseSireOfDamName')
            for horse in results:
                for field in NORMALIZE_FIELDS:
                    setattr(horse, field, self._normalize_name(getattr(horse, field, None), roman_nummerals=True))
                if hasattr(horse, 'Rankings') and getattr(horse.Rankings, 'RankingOC', None):
                    for ranking in horse.Rankings.RankingOC:
                        ranking.AthleteFamilyName = self._normalize_name(getattr(ranking, 'AthleteFamilyName', None))
                        ranking.HorseName = self._normalize_name(getattr(ranking, 'HorseName', None), roman_nummerals=True)
        return results

    def search_horse_trainers(self, horse_fei_code=None, person_fei_id=None, eval_date=None, page_number=1):
        """
        Search for horse trainer records

        :param horse_fei_code: The FEI identifier of the horse filters the records and returns only trainers
        linked to this horse. It maybe null.
        :param person_fei_id: The FEI identifier of the person filters the records and returns only the trainer
        having this ID. It may be null
        :param eval_date: The evaluation date filters the horse trainer records and returns only those whose period
        is active at this evaluation date. It may be null.
        :param page_number: Which page to retrieve. 1 = 1 - 100, 2 = 101 - 200
        :return: returns an array of zero or more HorseTrainer objects.
        """
        response = self.get_organizer_data('searchHorseTrainers',
            HorseFEICode=horse_fei_code, PersonFEIID=person_fei_id, EvalDate=eval_date, PageNumber=page_number)
        results = response.HorseTrainer if hasattr(response, 'HorseTrainer') else []
        if self.normalize:
            for trainer in results:
                trainer.CompleteName = self._normalize_name(getattr(trainer, 'CompleteName', None), roman_nummerals=True)
                trainer.FamilyName = self._normalize_name(getattr(trainer, 'FamilyName', None))
        return results

    def find_event(self, id='', show_date_from=None, show_date_to=None, venue_name='', nf='', discipline_code='',
                   level_code='', is_indoor=None):
        """
        Find FEI events based on a certain search criteria.
        :param id: FEI show/event/competition ID.
        :param show_date_from: Filter shows from this date up.
        :param show_date_to: Filter shows from this date down.
        :param venue_name: The name of the place where the show is held.
        :param nf: Country code of the national federation.
        :param discipline_code: Filter shows based on discipline.
        :param level_code: Filter shows based on level.
        :param is_indoor: Filter indoor / outdoor shows.
        :return: Return value: A list of FEI events
        """
        result = self.get_organizer_data(
            'findEvent',
            ID=id, ShowDateFrom=show_date_from, ShowDateTo=show_date_to, VenueName=venue_name, NF=nf,
            DisciplineCode=discipline_code, LevelCode=level_code, IsIndoor=is_indoor)
        if hasattr(result, 'ShowOC'):
            return result.ShowOC
        return []

    def download_results(self, id):
        """
        Download XML results from the FEI. (You need permission from the FEI
         to download results from an event.
        :param id: FEI event/competition ID.
        :return: A string containing the information in FEI XML.
        """
        result = self._ows_client.service.downloadResults(id)
        self._handle_messages(result)
        return result

    def upload_results(self, result_xml_data):
        """
        Upload results to the FEI. (You need permission from the FEI to
        upload results to the FEI.
        :param result_xml_data: Base64Encoded FEI result file.
        :return:
            FileID = can be used to confirm uploaded results
            Results = String indicating if the uploaded succeeded.
                ERR = An error was found while processing the validation
                MAN = An error was found while processing the mandotory check
                OKW = It is ok for saving, but there are warnings
                OKD = the saving has been done
        """
        return self._ows_client.service.uploadResults(result_xml_data)

    def confirm_upload_results(self, file_id):
        """
        Confirm uploaded results. This is only needed when results returned OK with warnings.
        :param file_id: The FileID return by the uploadResults routine.
        :return: True if the saving has been done.
        """
        return self._ows_client.service.confirmUploadResults(file_id)

    def submit_results(self, id):
        """
        Submit the results to the FEI validation for a given event or a
         given competition.
        :param id: FEI event/competition ID.
        :return: True if the results have been successfully submitted.
        """
        return self._ows_client.service.submitResults(id)

    def get_version(self):
        """
        Return the version string of the Core Application software
        :return: Returns a string containing the [major.minor.revision] number.
        If no return value is recieved or the call times out then the web service is not working
        and should not be used.
        """
        return self.get_common_data('getVersion')

    def get_lookup_date_list(self):
        """
        Retrieve a list of cached information types, and the date each was last modified.
        :return: Returns an array of LookupDate objects.
        Each LookupDate object contains the name of an object type and the most recent date of modification
        for any of the lookup records held in that object type. Client applications should keep these
        lookup records in a local cache to improve performance, and reduce server load.
        For each of these LookupDate objects, there is a corresponding method get<LookupDate.Name>List()
        that retrieves a list of all records of that type.
        """
        result = self.get_common_data('getLookupDateList')
        return result.LookupDate


    def get_country_list(self):
        """
        Retrieve a list of countries.
        :return: Returns an array of Country objects.
        Returns an array of Country objects containing all countries and their corresponding
        names and nationally recognized codes (NOC).
        """
        result = self.get_common_data('getCountryList')
        return result.Country

    def get_dicipline_list(self):
        """
        Retrieve a list of discipline records
        :return: Returns an array of Discipline objects.
        """
        result = self.get_common_data('getDisciplineList')
        return result.Discipline

    def get_issuing_body_list(self):
        """
        Retrieve a list of document issuing bodies.
        :return: Returns an array of DocIssuingBody objects.
        """
        result = self.get_common_data('getDocIssuingBodyList')
        return result.DocIssuingBody

    def get_national_federation_list(self):
        """
        Retrieve a list of National Federations.
        :return: Returns an array of NationalFederation objects.
        """
        result = self.get_common_data('getNationalFederationList')
        return result.NationalFederation

    def get_horse_name_kind_change_list(self):
        """
        Retrieve a list of kind of changes for the name of a horse.
        :return: Returns an array of KindChange objects.
        """
        result = self.get_common_data('getHorseNameKindChangeList')
        return result.KindChange

    def get_document_type_list(self):
        """
        Retrieve a list of extension for the document type.
        :return: Returns an array of DocumentType objects.
        """
        result = self.get_common_data('getDocumentTypeList')
        return result.DocumentType

    def get_language_list(self):
        """
        Retrieve a list of languages used for mailings.
        :return: Returns an array of Language objects.
        """
        result = self.get_common_data('getLanguageList')
        return result.Language

    def get_category_list(self):
        """
        Retrieve a list of categories for an event.
        :return: Returns an array of Category objects containing all
        category values and their corresponding names.
        """
        result = self.get_common_data('getCategoryList')
        return result.Category

    def get_address_name_list(self):
        """
        Retrieve a list of address types.
        :return: Returns an array of AddressName objects containing all addresstypes.
        """
        result = self.get_common_data('getAddressNameList')
        return result.AddressName

    def get_horse_gender_list(self):
        """
        Retrieve a list of horse genders.
        :return: Returns an array of Gender objects containing all horse genders.
        """
        result = self.get_common_data('getHorseGenderList')
        return result.Gender

    def get_horse_fei_id_type_list(self):
        """
        Retrieve a list of horse FEI ID types.
        :return: Returns an array of FEIIDType objects containing all horse FEI ID types.
        """
        result = self.get_common_data('getHorseFEIIDTypeList')
        return result.FEIIDType

    def get_person_gender_list(self):
        """
        Retrieve a list of person genders.
        :return: Returns an array of Gender objects containing all person genders.
        """
        result = self.get_common_data('getPersonGenderList')
        return result.Gender

    def get_person_civility_list(self):
        """
        Retrieve a list of person civilities.
        :return: Returns an array of Person Civility objects containing all person civilities.
        """
        result = self.get_common_data('getPersonCivilityList')
        return result.Civility

    def get_official_function_list(self):
        """
        Retrieve a list of official functions.
        :return: Returns an array of OfficialFunction objects containing all additional functions.
        """
        result = self.get_common_data('getOfficialFunctionList')
        return result.OfficialFunction

    def get_official_status_list(self):
        """
        Retrieve a list of official status.
        :return: Returns an array of OfficialStatus objects containing all additional status.
        """
        result = self.get_common_data('getOfficialStatusList')
        return result.OfficialStatus

    def get_additional_role_list(self):
        """
        Retrieve a list of additional roles.
        :return: Returns an array of AdditionalRole objects containing all additional roles.
        """
        result = self.get_common_data('getAdditionalRoleList')
        return result.AdditionalRole

    def get_message_type_list(self):
        """
        Retrieve a list of error message types and warnings.
        :return: Returns an array of MessageType objects.
        """
        result = self.get_common_data('getMessageTypeList')
        return result.MessageType

    def get_season_list(self, discipline_code='S'):
        """
        Returns the list of World Cup seasons for a given discipline
        (jumping and dressage seasons, currently).
        Those season strings can then be used as input in getLeagueList.
        :param discipline_code: Specify which World Cup seasons will be returned:
            S for World Cup Jumping seasons and D for World Cup Dressage seasons.
        :return: The method returns an array of strings corresponding each
        to a World Cup season of the chosen discipline.
        """
        result = self.get_common_data('getSeasonList', DisciplineCode=discipline_code)
        return result.string

    def get_league_list(self, discipline_code='S', season_code=None):
        """
        Returns a list of Leagues for a given discipline and season
        :param discipline_code: Specify which World Cup leagues will be returned:
            S for World Cup Jumping leagues and D for World Cup Dressage leagues.
        :param season_code: Specify a World Cup season.
            Only the leagues valid during this season will be returned.
        :return: The method returns an array of strings corresponding each to a World Cup
            league of the chosen discipline.
        """
        result = self.get_common_data('getLeagueList', DisciplineCode=discipline_code,
                                      SeasonCode=season_code)
        return result.League


class FEIEntrySystemClient:
    def __init__(self):
        self._base_url = config.FEI_ES_BASE_URL

    def _parse_date(self, value):
        if not value:
            return None
        try:
            return date(*(time.strptime(value, '%Y-%m-%d')[0:3]))
        except ValueError:
            return None

    def _parse_date_time(self, value):
        if not value:
            return None
        try:
            return datetime(*(time.strptime(value, '%Y-%m-%d %H:%M:%S')[0:6]))
        except ValueError:
            return None

    def _parse_athletes(self, root):
        athletes = dict()
        for el in root.iter('{http://www.fei.org/Entry}Athlete'):
            athlete = dict(
                birth_date=self._parse_date(el.get('BirthDate', '')),
                competing_for=el.get('CompetingFor'),
                fei_id=int(el.get('FEIID')),
                family_name=normalize_name(el.get('FamilyName')),
                first_name=el.get('FirstName'),
                NF_id=el.get('NFID'),
                gender=el.get('Gender'),
                time_stamp=int(el.get('TimeStamp', 0))
            )
            contact = el.find('{http://www.fei.org/Entry}ContactPerson')
            if contact:
                athlete['email'] = contact.get('Email')
                athlete['phone'] = contact.get('MobilePhone')
                athlete['contact_name'] = contact.get('Name')
                athlete['contact_quality'] = contact.get('Quality')
            athletes[athlete['fei_id']] = athlete
        return athletes

    def _parse_horses(self, root):
        horses = dict()
        for el in root.iter('{http://www.fei.org/Entry}Horse'):
            horse = dict(
                fei_id=el.get('FEIID'),
                id_type=el.get('IDType'),
                bedding=el.get('Bedding'),
                birth_date=self._parse_date(el.get('BirthDate', '')),
                birth_country=el.get('BirthCountry'),
                breeder=el.get('Breeder'),
                chip_id=el.get('ChipID'),
                color=el.get('Color'),
                color_complement=el.get('ColorComplement'),
                dam=normalize_name(el.get('Dam'), True),
                gender=el.get('Gender'),
                name=normalize_name(el.get('Name'), True),
                owner=normalize_name(el.get('Owner')),
                pony=el.get('Pony', 'false') == 'true',
                sex=el.get('Sex'),
                shorten_name=el.get('ShortenName'),
                sire=normalize_name(el.get('Sire'), True),
                sire_of_dam=normalize_name(el.get('SireOfDam'), True),
                stallion=el.get('Stallion') == 'true',
                studbook=el.get('StudBook'),
                studbook_code=el.get('StudBookCode'),
                NF_id=el.get('NFID'),
                UELN=el.get('UELN'),
                time_stamp=int(el.get('TimeStamp', 0))
            )
            horses[horse['fei_id']] = horse
            horse['ownership'] = self._parse_owners(el)
        return horses

    def _parse_owners(self, root):
        owners = []
        for el in root.iter('{http://www.fei.org/Entry}Owner'):
            owner = dict(
                corperation_name=el.get('CorporationName'),
                family_name=el.get('FamilyName'),
                first_name=el.get('FirstName')
            )
            owners.append(owner)
        return owners


    def _parse_event_entries(self, root, event_code=None):
        events = dict()
        for el in root.iter('{http://www.fei.org/Entry}Event'):
            if event_code and el.get('FEIID', '').lower() != event_code:
                continue  # skip events that are not part of the query

            event = dict(
                fei_id=el.get('FEIID'),
                athlete_max_age=el.get('AthletesMaxAge'),
                athlete_min_age=el.get('AthletesMinAge'),
                category=el.get('Category'),
                category_code=el.get('CategoryCode'),
                code=el.get('Code'),
                definite_entries_date=self._parse_date(el.get('DefiniteEntriesDate', '')),
                discipline=el.get('Discipline'),
                discipline_code=el.get('DisciplineCode'),
                end_date=self._parse_date(el.get('EndDate', '')),
                horse_max_age=el.get('HorsesMaxAge'),
                horse_min_age=el.get('HorsesMinAge'),
                indoor=el.get('Indoor', 'false') == 'true',
                last_date_substitution=self._parse_date(el.get('LastDateSubstitution', '')),
                level=el.get('Level'),
                level_code=el.get('LevelCode'),
                official_team=el.get('OfficialTeam', 'false') == 'true',
                start_date=self._parse_date(el.get('StartDate', '')),
                start_date_subst_addit_OC=self._parse_date(el.get('StartDateSubstAdditOC', '')),
                time_stamp=int(el.get('TimeStamp', 0))
            )
            events[event['fei_id']] = event
            entries = []
            event['entries'] = entries
            for entryEl in el.iter('{http://www.fei.org/Entry}AthleteEntry'):
                entry = self._parse_athlete_entry(entryEl)
                entries.append(entry)
                horses = []
                for horseEl in entryEl.iter('{http://www.fei.org/Entry}HorseEntry'):
                    horses.append(self._parse_entry(horseEl))
                entry['horses'] = horses
        return events

    def _parse_entry(self, el):
        entry = dict(
            acceptation_date=self._parse_date_time(el.get('AcceptationDate', '')),
            accepted=el.get('Accepted') == 'true',
            competitions=el.get('Competitions'),
            definite=el.get('Definite') == 'true',
            definite_entry_date=self._parse_date(el.get('DefiniteEntryDate', '')),
            fei_id=el.get('FEIID'),
            NF_comment=el.get('NFComment'),
            nominated=el.get('Nominated') == 'true',
            nominated_entry_date=self._parse_date_time(el.get('NominatedEntryDate', '')),
            pending=el.get('Pending') == 'true',
            rejected=el.get('Rejected') == 'true',
            rejection_comment=el.get('RejectionComment'),
            rejection_date=self._parse_date_time(el.get('RejectionDate', '')),
            substituted=el.get('Substituted') == 'true',
            withdrawn=el.get('Withdrawn') == 'true',
            time_stamp=int(el.get('TimeStamp', 0))
        )
        return entry

    def _parse_athlete_entry(self, el):
        entry = self._parse_entry(el)
        entry['fei_id'] = int(entry['fei_id'])
        entry['borrowed_horses'] = el.get('BorrowedHorses') == 'true'
        entry['entering_nf'] = el.get('EnteringNF')
        entry['team'] = el.get('Team')
        return entry

    def _parse_show(self, root):
        for el in root.iter('{http://www.fei.org/Entry}ShowEntries'):
            show_xml = el.find('{http://www.fei.org/Entry}Show')
            if not show_xml:
                return None
            show = dict(
                end_date=self._parse_date(show_xml.get('EndDate', '')),
                start_date=self._parse_date(show_xml.get('StartDate', '')),
                fei_id=show_xml.get('FEIID'),
                type=show_xml.get('Type'),
                type_code=show_xml.get('TypeCode'),
                time_stamp=int(show_xml.get('TimeStamp', 0))
            )
            venue_xml = show_xml.find('{http://www.fei.org/Entry}Venue')
            if venue_xml:
                venue = dict(
                    country=venue_xml.get('Country'),
                    country_NOC=venue_xml.get('CountryNOC'),
                    name=venue_xml.get('Name')
                )
                show['venue'] = venue
            return show


    def _parse_root(self, content):
        try:
            return ET.fromstring(content)
        except ParseError:
            return None

    def _parse_entry_file(self, content, event_code=None):
        root = self._parse_root(content)
        if root is None:
            return {}
        show = self._parse_show(root)
        if not show:
            return
        show['athletes'] = self._parse_athletes(root)
        show['horses'] = self._parse_horses(root)
        if event_code:
            show['events'] = self._parse_event_entries(root, event_code.lower())
        else:
            show['events'] = self._parse_event_entries(root)
        return show

    def get_event_entries(self, event_code):
        url = urljoin(self._base_url, 'index.php')
        response = requests.get(url, params={'doc': 'EntryFileDownload', 'event_id': event_code})
        if response.status_code == 200:
            return self._parse_entry_file(response.content, event_code)

    def get_show_entries(self, show_code):
        url = urljoin(self._base_url, 'index.php')
        response = requests.get(url, params={'doc': 'EntryFileDownload', 'show_id': show_code})
        if response.status_code == 200:
            return self._parse_entry_file(response.content)


class FEIEntrySystem3Client:
    def __init__(self, username=None, password=None):
        logger.info('initialize FEI Entry System V3 Client')
        self._username = username if username else config.FEI_WS_USERNAME
        self._password = password if password else config.FEI_WS_PASSWORD
        self._base_url = config.FEI_ESV3_BASE_URL
        self._session = requests.session()
        self._session.headers.update({'Cache-Control': "no-cache", "Content-Type": "application/json"})
        self._authenticate()

    def _authenticate(self):
        if not self._username or not self._password:
            raise fei_errors.FEIWSConfigException('Could not login: username and password are empty.')
        url = urljoin(self._base_url, '/login')
        response = self._session.post(
            url,
            data=json.dumps({'username': self._username, 'password': self._password})
        )

        if response.status_code == 400:  # Bad Request
            data = response.json()
            raise fei_errors.FEIWSApiException(data['message'], 400)
        elif response.status_code == 401:  # Bad Password
            raise fei_errors.FEIWSAuthException('Could not login: PasswordNotMatch', 401)
        elif response.status_code == 200:
            data = response.json()
            self._session.headers.update({'Authorization': "Bearer {}".format(data['token'])})
            return
        raise fei_errors.FEIWSApiException("Could not authenticate", 400)

    def _handle_error(self, response, data=None):
        if response.status_code > 400:
            if data and 'message' in data and 'code' in data:
                raise fei_errors.FEIWSApiException(data['message'], data['code'])
            raise fei_errors.FEIWSApiException('Bad Response', response.status_code)
        return response

    def _handle_json_response(self, response):
        try:
            data = response.json()
        except ValueError as e:
            raise fei_errors.FEIWSApiException('No JSON object could be decoded', 400)
        self._handle_error(response, data)
        return data

    def set_session(self, fei_id, password=None):
        """
        Session route to set or change the FEI user associated to requests. A valid Application token is required.
        :param fei_id: fei_id or FEI User id
        :param password: If set use password to authenticate, else only FEI_ID(NF ONLY)
        :return: A response object
        """
        url = urljoin(self._base_url, '/sessions')
        if not password:
            data = json.dumps({'fei_id': fei_id})
        else:
            data = json.dumps({'username': fei_id, 'password': password})
        response = self._session.post(url, data=data)
        self._handle_error(response)
        if response.status_code == 200:
            self._session.headers.update({'Authorization': response.headers['Authorization']})
        return response

    def set_act_as(self, act_as):
        """
        Route to change the role the current user will act as if the user is allowed to act with multiple roles (FEI, OC, NF, Athlete etc.)
        :param act_as: New role to use. Possible values: “fei”, “oc”, “nf”, “official”, “athlete”, “ath_manager or “groom”
        :return: Response object
        """
        url = urljoin(self._base_url, '/sessions')
        response = self._session.post(url, data=json.dumps({'act_as': act_as}))
        self._handle_error(response)
        if response.status_code == 200:
            self._session.headers.update({'Authorization': response.headers['Authorization']})
        return response

    def get_authorizations(self):
        """
        Returns the entry actions the connected user can perform depending on his permissions.
        :return: Array of Entry action codes
        """
        url = urljoin(self._base_url, '/user/authorizations')
        response = self._session.get(url)
        return self._handle_json_response(response)

    def get_show_entries(self, show_code, **kwargs):
        """
        Return the list of entries of a show for session user
        :param show_code: Show to retrieve.
        :param kwargs: Possible parameters
            <page>: page number.
            <items_per_page>: Items returned per page. Accepted values: 1 to 5000
            <sort>: String to sort results.
            <entries_for_nf>: NF code NOC. Filter entries from this NF.
            <team>: Search entries with corresponding team.
            <athlete_fei_id>: Search entries concerning only the given athlete.
            <horse_fei_id>: Search entries concerning only the given horse. (only for Web and Mobile Apps)
            <no_pagination>: 1 if pagination is not required. The API will returns the number of items_per_page.
            <list_type>: One of EntryListType. (from_invitation_oc, waiting, pending, accepted, rejected, all,
                all_myinvitations, no_show, only_empty_slot, all pr_accepted, pr_minitour_accepted, pr_pending,
                accept_ath, reject_ath, accept_hor, reject_hor, accept_subst_ath, reject_subst_ath, accept_subst_hor,
                reject_subst_hor)
        :return: Array of Entry elements.
        """
        url = urljoin(self._base_url, '/user/shows/{show_code}/entries'.format(show_code=show_code))
        response = self._session.get(url, params=kwargs)
        return self._handle_json_response(response)

    def get_event_entries(self, event_code, **kwargs):
        """
        Returns the list of entries of an event for session user. A valid API Token is required.
        Athlete session users can only request data for their entries.
        NF can receive entries for their NF.
        OC can receive entries with statuses : waiting, accepted, withdrawn, rejected.
        Actions on entries may depend on session user and event status. (Read Only, Consultation mode...).
        :param event_code: Event Code to retrieve.
        :param kwargs: contains the params to include in the url. Possible params:
            <page>: Page number
            <items_per_page>: Items returned per page. Accepted values: 1 to 5000
            <sort>: String to sort results.
            <entries_for_nf>: NF code NOC. Filter entries from this NF.
            <list_type>: One of EntryListType.
            <team>: Search entries with corresponding team.
            <athlete_fei_id>: Search entries concerning only the given athlete.
        :list_types: from_invitation_oc, waiting, pending, accepted, rejected, all,
                all_myinvitations, no_show, only_empty_slot, all pr_accepted, pr_minitour_accepted, pr_pending,
                accept_ath, reject_ath, accept_hor, reject_hor, accept_subst_ath, reject_subst_ath, accept_subst_hor,
                reject_subst_hor
        :return: Array of Entry elements.
        """
        url = urljoin(self._base_url, '/user/events/{event_id}/entries'.format(event_id=event_code))
        response = self._session.get(url, params=kwargs)
        return self._handle_json_response(response)

    def search_athlete(self, event_code, **kwargs):
        """
        Return athlete list for this event and for current session user. Athletes cannot list athletes.
        NF can list only athlete competing for the current NF.
        :param event_code: Event code to retrieve
        :param kwargs: contains the params to include in the url. Possible params:
            <page>: Page number
            <items_per_page>: Items returned per page. Accepted values: 1 to 5000
            <sort>: String to sort results.
            <athlete>: Athlete name or FEI ID.
            <athlete_mode>: Athlete name search mode : [contains|start_with], default is 'start_with'.
            <list_mode>: Infos returned : [wo_checking_entries|all], default is 'all' (`wo_checking_entries` not return entries)
            <registered>: Accepted values: 1 or 0
            <age_limit>: Accepted values: 1 or 0
            <qualified>: Accepted values: 1 or 0
            <no_pagination>: 1 if pagination is not required. The API will returns the number of items_per_page.
            <active_athlete>: Values : active // inactive // all. Default: active. Only returns athlete with the provided state.
            <show_host_athletes>: NF User only, returns hosted athletes or not. Default value = 1 (true).
        :return: Array of “SearchAthlete” objects
        """
        url = urljoin(self._base_url, '/user/events/{event_code}/athletes'.format(event_code=event_code))
        response = self._session.get(url, params=kwargs)
        return self._handle_json_response(response)

    def search_horses(self, event_code, **kwargs):
        """
        Searches horses in the requested event and for current session user. A valid application Token is required.
        Info on blocked horses and registrations may also be returned.
        :param event_code: Event code to retrieve
        :param kwargs: contains the params to include in the url. Possible params:
            <page>: Page number
            <items_per_page>: Items returned per page. Accepted values: 1 to 5000
            <sort>: How to sort. Default is name. Values(name, fei_id).
            <horse>: Athlete name or FEI ID.
            <favorite_horses_athlete>: Returns the horses with imported results for the given athlete FEI ID. Only the last 12 months results are checked.
            <registered>: Accepted values: 1 or 0
            <age_limit>: Accepted values: 1 or 0
            <nf_noc>: NF NOC code or empty for all. Default value is session user’s NF
        :return: Array of “SearchHorse” objects
        """
        url = urljoin(self._base_url, '/user/events/{event_code}/horses'.format(event_code=event_code))
        response = self._session.get(url, params=kwargs)
        return self._handle_json_response(response)