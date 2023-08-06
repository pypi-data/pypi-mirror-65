class FEIWSConfigException(Exception):
    pass


class FEIWSAuthException(Exception):
    pass


class FEIWSApiException(Exception):
    def __init__(self, message, code):
        self.code = code
        super(FEIWSApiException, self).__init__(message)


# These message types are generated from the client.get_message_type_list API call.
FEI_MESSAGE_TYPES = [{
    'Id': 'InvalidAddressName',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Address Name does not exist'
}, {
    'Id': 'PermissionDenied',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The connected user is not authorized to perform this operation.'
}, {
    'Id': 'InvalidAdmSBCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "The Studbook DB of the connected user doesn't match the requested Studbook Performances."
}, {
    'Id': 'InvalidCountryCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Country Code is not a valid value'
}, {
    'Id': 'InvalidBirthName',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The BirthName value has an incorrect format'
}, {
    'Id': 'InvalidCommercialName',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Commercial prefix or suffix value has an incorrect format'
}, {
    'Id': 'InvalidCurrentName',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Current Name value has an incorrect format'
}, {
    'Id': 'InvalidDateBirth',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Date of Birth value is too old or in the future.'
}, {
    'Id': 'InvalidDateCastration',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Date of Castration but is incoherent with the current date or Date of Birth or Date of Death.'
}, {
    'Id': 'InvalidDateDeath',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Date of Death value out of range'
}, {
    'Id': 'InvalidDateChronology',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The dates must be in a chronologic order (dateFrom <= dateTo)'
}, {
    'Id': 'InvalidDateRetirement',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Date of Retirement is out of range'
}, {
    'Id': 'InvalidDisciplineCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Discipline Code is not in the Discipline list'
}, {
    'Id': 'InvalidOrganizerNFCountryCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The NF Code for the Organizer NF is not in the National Federation list'
}, {
    'Id': 'NotAllowedOrganizerNFCountryCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'You can use only your own NF NOC code (or null) for the field "OrganizingNFCountryCode"'
}, {
    'Id': 'InvalidRiderCompetingForCountryCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Country Code for the Rider Competing For is not in the Country list'
}, {
    'Id': 'NotAllowedRiderCompetingForCountryCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'You can use only your own NF NOC code (or null) for the field "CompetingForCountryCode"'
}, {
    'Id': 'InvalidFile',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The format of the file is not correct.'
}, {
    'Id': 'InvalidMaxContentLength',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The content of the file is too big.'
}, {
    'Id': 'NotificationError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'An error occurred during the notification process. Please contact your administrator.'
}, {
    'Id': 'InvalidLeagueTypeCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The LeagueTypeCode is not one of the valid option.'
}, {
    'Id': 'InvalidSeasonCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The SeasonCode is not a valid one.'
}, {
    'Id': 'PermissionDeniedChangeStatus',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The change of status is refused for the following reasons, the record is in pending, cancelled or suspended status'
}, {
    'Id': 'InvalidStatus',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The current status of the record do not allow the requested modification'
}, {
    'Id': 'InvalidTicket',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The ticket is invalid or has expired. You must redo the add/update method invocation before reinvoking the confirm method.'
}, {
    'Id': 'PotentialDuplicateFound',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "One or more potential duplicates were found. Your data has not been commited. Please review the record you're trying to insert/update and, if it's adequat, confirm your operation by calling the corresponding confirm method, by providing the received ticket."
}, {
    'Id': 'ConcurrencyUpdateDetected',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Another user has changed these data'
}, {
    'Id': 'RidesDistancesAndSpeedsAreInvalid',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'There must be 2 rides of distances between 40-79 km and 2 rides of distances between 80-90 km at speeds of 16 kph or under.'
}, {
    'Id': 'ConflictWithExistingEntry',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'There is an existing entry related to the Novice Qualification.'
}, {
    'Id': 'DatesAreInvalid',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "The dates should not exceed today's date."
}, {
    'Id': 'HorseNotEndurance',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The horse must have an endurance registration.'
}, {
    'Id': 'FourNationalResults',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'There must be 4 national results.'
}, {
    'Id': 'ThreeQualifyingResultsAtMost',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'There must be three qualifying results at most (but less is possible).'
}, {
    'Id': 'HorseAtLeastEightYearsOldAtLastQualifyingResult',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'There must be three qualifying results at most (but less is possible).'
}, {
    'Id': 'TotalDistanceMustBe240KmAtLeast',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The total distance must be 240 km at least.'
}, {
    'Id': 'TimeSpanBetweenFisrtAndLastQualifyingResultMustBeAtMost36Months',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The time span between the first and the last results must be at most 36 months.'
}, {
    'Id': 'UnexpectedErrorOccured',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'An unexpected error occurred.'
}, {
    'Id': 'PersonNotEndurance',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The person must have an endurance registration.'
}, {
    'Id': 'MissingRoles',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The user does not have the authorization.'
}, {
    'Id': 'ConflictWithExistingNoviceQualification',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Novice Qualification should not have the same qualification start date as an existing one'
}, {
    'Id': 'AllFieldsAreRequired',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'All fields are mandatory.'
}, {
    'Id': 'NoviceQualificationDoesNotExist',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The provided data does not identify an existing Novice Qualification'
}, {
    'Id': 'DistanceIsNotValid',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Distance is not valid.'
}, {
    'Id': 'RankIsNotValid',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Rank is not valid.'
}, {
    'Id': 'AverageSpeedIsNotValid',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Average speed is not valid.'
}, {
    'Id': 'horseIsNotNoviceQualified',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The horse is not Novice Qualified'
}, {
    'Id': 'InvalidTimespanBetweenFirstAndLastResultHorse',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The timespan between the first and the last result must be between 1 year and 2 years'
}, {
    'Id': 'InvalidTimespanBetweenFirstAndLastResultAthlete',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The timespan between the first and the last result must be between 6 months and 2 years'
}, {
    'Id': 'RankPositionIsMandatory',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Rank position is mandatory'
}, {
    'Id': 'AverageSpeedIsMandatory',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Average speed is mandatory'
}, {
    'Id': 'EnduranceTrainerRequired',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'An endurance registered trainer is missing for the specified year'
}, {
    'Id': 'InvalidHeight',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Height of the horse is out of range'
}, {
    'Id': 'InvalidHorseAnyID',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Horse Any ID is too long. See detail for maximum length.'
}, {
    'Id': 'InvalidHorseFEICode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Horse FEI Code is not valid'
}, {
    'Id': 'InvalidHorseNF',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Horse is not administered by your NF'
}, {
    'Id': 'InvalidHorseNFCountry',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Upgrading to Passport is not possible for UE Horses - reference to the Veterinarian Rules, see in https://inside.fei.org/system/files/Letter-EU-NFs_May2011.pdf '
}, {
    'Id': 'InvalidDocGenderCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The value given for DocumentGenderCode is not valid'
}, {
    'Id': 'InvalidHorseIdentity',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The value given for HorseIdentityTypeCode is not valid'
}, {
    'Id': 'NoDocumentLine',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The type of document identified HorseIdentityTypeCode is not currently requested for this horse; check which document is requested'
}, {
    'Id': 'DocPartDoesNotMatchDocGender',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The value given for DocumentGenderCode is not compatible with the value given for HorseIdentityTypeCode'
}, {
    'Id': 'InvalidHorseFeiIDType',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Not a valid Horse Fei ID Type'
}, {
    'Id': 'InvalidIsCastrated',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The IsCastrated value is incompatible with the date of castration'
}, {
    'Id': 'InvalidPonyHeight',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The IsPony value has been set true, but the height is too tall for a pony'
}, {
    'Id': 'InvalidReasonNF',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Excepting for changes on birth name or shorten name, the changes in names are invoiced.'
}, {
    'Id': 'InvalidRequest',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The request is not valid as you are already administering this horse or person. '
}, {
    'Id': 'InvalidShortName',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The ShortName value has an incorrect format'
}, {
    'Id': 'InvalidYear',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Year number is out of range'
}, {
    'Id': 'InvalidRecognitionCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The RecognitionCode must be empty'
}, {
    'Id': 'InvalidRecognitionCodeRO',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The recognition code cannot be changed.'
}, {
    'Id': 'InvalidDateIssuingOutOfRange',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Issuing Date is out of range (01.01.1990 and 31.12.2006)'
}, {
    'Id': 'InvalidDateIssuing',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The DateIssuing is not setted between the DateBirth and today'
}, {
    'Id': 'InvalidIssuingBodyCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The IssuingBodyCode cannot be empty.'
}, {
    'Id': 'InvalidIssuingBodyCodeRO',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The IssuingBodyCode cannot be changed.'
}, {
    'Id': 'InvalidRequestOneIsInPending',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'A request is already in pending status'
}, {
    'Id': 'InvalidRegOnlyWithOldFEIID',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'You cannot add an existing horse with only a registration number'
}, {
    'Id': 'InvalidShortNameRequiredFromCompleteName',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'You must give a shorten name as the complete name longer than 20 characters'
}, {
    'Id': 'InvalidOldFEICode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The old FEI ID has an invalid format.'
}, {
    'Id': 'InvalidOldFEICodeExisting',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The given old FEI ID is already in use in the system.'
}, {
    'Id': 'InvalidUpgradeOperation',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Only horses without a passport or a recognition card can be upgraded.'
}, {
    'Id': 'InvalidDocType',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The document extension is not allowed.'
}, {
    'Id': 'InvalidAlreadyUploaded',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'You cannot upload a diagram as the horse already has a diagram.'
}, {
    'Id': 'HorseAlreadyRegistered',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The horse is already registered in this discipline'
}, {
    'Id': 'InvalidOwnerBeginDateBeforeBirthday',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The OwnerBeginDate must not be before the birthDate'
}, {
    'Id': 'InvalidOwnerBeginDateInFuture',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The OwnerBeginDate must not be in the future'
}, {
    'Id': 'InvalidOwnerBeginDateBeforeLastOwner',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The OwnerBeginDate must not be before the OwnerBeginDate of the previous owner'
}, {
    'Id': 'InvalidUELNPattern',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The pattern of the UELN is incorrect'
}, {
    'Id': 'UELNUniquenessViolation',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The UELN is a unique number, your horse cannot have the same UELN as another horse. Please contact the FEI'
}, {
    'Id': 'ChipIDUniquenessViolation',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The chip ID should be unique.'
}, {
    'Id': 'ObsoleteFunction',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Acces denied'
}, {
    'Id': 'MicrochipIsMandatory',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The microchip number is mandatory if the horse has been created after the 01/01/2013'
}, {
    'Id': 'MicrochipIsAlreadySet',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Microchip value cannot be changed anymore once a value has been provided. Please fill the form at https://inside.fei.org/fei/your-role/veterinarians/passports/microchips and return it to the FEI.'
}, {
    'Id': 'MicrochipIsAlreadySetNoUrl',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Microchip value cannot be changed anymore once a value has been provided.'
}, {
    'Id': 'MicrochipId',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'MicrochipId'
}, {
    'Id': 'InvalidStickerType',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The sticker type is not supported.'
}, {
    'Id': 'NoSuchStickerAvailable',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'No such sticker available for this horse.'
}, {
    'Id': 'NoLongerAvailable',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The limited period to download an original sticker is expired therefore it cannot anymore be downloaded.'
}, {
    'Id': 'InvalidSexCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The provided SexCode is not among the available values.'
}, {
    'Id': 'InvalidTrainerPeriod_2',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The new starting date must be greater than the starting date of the actual horse trainer'
}, {
    'Id': 'InvalidTrainerPeriod_3',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The last day of horse registration year is undefined'
}, {
    'Id': 'InvalidTrainerPeriod_4',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The new start date must be the next day after the last horse trainer end date'
}, {
    'Id': 'InvalidTrainerPeriod_5',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The new end date cannot be greater than the end of the latest horse registration year'
}, {
    'Id': 'InvalidTrainerPeriod_6',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The new end date cannot be smaller than the end of the current registration year'
}, {
    'Id': 'InvalidTrainerPeriod_7',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'This person cannot be chosen as a trainer'
}, {
    'Id': 'GetHorseOwnerWSDisabled',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The method getHorseOwner is deprecated. Use getHorseOwnership instead.'
}, {
    'Id': 'InvalidStudbookCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The studbook code is not valid'
}, {
    'Id': 'AssignHorseOwnerWSDisabled',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The method assignHorseOwner is deprecated. Use assignHorseOwnership instead.'
}, {
    'Id': 'AddOldOwnerFiedsDisabledUseOwnership',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Horse.Ownership should be used to create an owner. Other owner fields in Horse are deprecated.'
}, {
    'Id': 'TotalOwnershipPercentageMustBe100',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'If the ownership percentages are filled, their total must be of 100%'
}, {
    'Id': 'AllPercentageMustBeProvided',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'If at least one percentage is filled, all percentages must be filled.'
}, {
    'Id': 'InvalidDateFrom',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'DateFrom must be greater than the last Since owner date and smaller or equal than today.'
}, {
    'Id': 'HorseNotFound',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Horse not found.'
}, {
    'Id': 'MemberNotFound',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Member (Corporation/Person) not found.'
}, {
    'Id': 'PercentageMustBeEmpty',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Percentage must be empty or different of 0.'
}, {
    'Id': 'HorseHasBeenMigratedToNewOwnershipFormat',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'This method cannot be called on a horse that has an ownership in the new format. Please use the assignHorseOwnership method instead.'
}, {
    'Id': 'UpdateForbiddenSire',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The update of the sire (Name or UELN) of this horse is locked, because a pedigree horse has been linked to it.'
}, {
    'Id': 'UpdateForbiddenDam',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The update of the dam (Name or UELN) of this horse is locked, because a pedigree horse has been linked to it.'
}, {
    'Id': 'UpdateForbiddenSireOfDam',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The update of the sire of dam (Name or UELN) of this horse is locked, because a pedigree horse has been linked to it.'
}, {
    'Id': 'InvalidKindOfName',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid Kind Of Name'
}, {
    'Id': 'BirthNameMustMatchCurrentName',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Birth Name must match Current Name'
}, {
    'Id': 'BirthNameMustDifferCurrentNameOrCommercialNameMustBeSet',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Birth Name must differ from Current Name or Commercial Name must be provided'
}, {
    'Id': 'InvalidBirthDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Birth date is not valid, see linked pedigree horses.'
}, {
    'Id': 'InvalidGender',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Gender is not valid, see linked pedigree horses.'
}, {
    'Id': 'InvalidOwnershipNationality',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'NationalityOfOwnership must be one of the Nationality of the Owners'
}, {
    'Id': 'InvalidMemberStatus',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'At least one member status is invalid.'
}, {
    'Id': 'InvalidMemberAddress',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'At least one member address is invalid.'
}, {
    'Id': 'InvalidAddressAlreadyExist',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Address already exists'
}, {
    'Id': 'OwnershipAddress',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'As this address is used in at least one horse ownership, you cannot change it. If you need to make a correction of that address, please contact FEI.'
}, {
    'Id': 'InvalidBusinessEmailAddress',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The BusinessEmailAddress is not correctly formatted'
}, {
    'Id': 'InvalidHomepage',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Homepage URL is not correctly formatted'
}, {
    'Id': 'InvalidIsActive',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The IsActive cannot be false because a date of death or date of retirement is given.'
}, {
    'Id': 'InvalidIsMailingAddress',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The IsMailingAddress can not be modified'
}, {
    'Id': 'MissingMailingAddress',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The MailingAddress must be set'
}, {
    'Id': 'InvalidMailingLanguage',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Mailing Language value is not valid'
}, {
    'Id': 'MissingNationalities',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'One or more nationality is required'
}, {
    'Id': 'MissingDateOfBirth',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Birth date is mandatory if the person is an Athlete, a Trainer or an Official'
}, {
    'Id': 'InvalidGroupCodes',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Only the group codes given in the Detail property of this message can be modified by the NF'
}, {
    'Id': 'ChangeGroupCodeError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'You are not authorized to change the group codes given in the Detail property'
}, {
    'Id': 'CompetingForLocked',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'CompetingFor is locked.'
}, {
    'Id': 'CompetingForMustBeEmpty',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'You should not specify the CompetingFor if you are not creating an Athlete record.'
}, {
    'Id': 'InvalidEventingCategory',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'InvalidEventingCategory'
}, {
    'Id': 'InvalidPersonAnyID',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Person Any ID is too long. See detail for maximum length.'
}, {
    'Id': 'InvalidPersonFEIID',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The PersonFEIID is not valid'
}, {
    'Id': 'InvalidNFNoc',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The NF NOC is not valid'
}, {
    'Id': 'InvalidAddressPerson',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Person Address Name does not exist'
}, {
    'Id': 'InvalidPrivateEmailAddress',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The PrivateEmailAddress is not correctly formatted'
}, {
    'Id': 'EmailLockedByUserStatus',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The email is locked due to the user status (the person has a pending, active or suspended user account).'
}, {
    'Id': 'PersonAlreadyRegistered',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The person is already registered in this discipline'
}, {
    'Id': 'MissingLeague',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "The WC person's league must be set first"
}, {
    'Id': 'LeagueAlreadySet',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "The WC person's league is already set in this discipline"
}, {
    'Id': 'OnlyOneLeague',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "The WC person's league can be set only if several natural leagues exist in this discipline"
}, {
    'Id': 'NoLeague',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "No WC person's league defined"
}, {
    'Id': 'InvalidLeague',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'This league is unknown in this discipline'
}, {
    'Id': 'InvalidGenderCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The provided GenderCode is not among the available values.'
}, {
    'Id': 'InvalidNationalities',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'At least one nationality is invalid'
}, {
    'Id': 'GroupCodesNotFound',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The value in GroupCodes contains at least one invalid code'
}, {
    'Id': 'PersonUpgradeNotAllowed',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'PersonUpgradeNotAllowed'
}, {
    'Id': 'TrainerAlreadyRegistered',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The trainer is already registered'
}, {
    'Id': 'OwnerOwnsAHorse',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The owner group cannot be removed since the person is owning a horse.'
}, {
    'Id': 'personIsNotNoviceQualified',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The person is not Novice Qualified'
}, {
    'Id': 'CorporationContactIsContact',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The corporation contact group cannot be removed since the person is currently person of contact for a corporation.'
}, {
    'Id': 'NotAllowedToRemoveANationality',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'It is not allowed to remove a nationality from a person. If a nationality is wrong, please contact the FEI.'
}, {
    'Id': 'DuplicateNationality',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Duplicate nationality was found.'
}, {
    'Id': 'InvalidCorporationFEIID',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'This corporation FEIID is not valid'
}, {
    'Id': 'InvalidCorporationAddress',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'At least one address is invalid.'
}, {
    'Id': 'InvalidAddressCountry',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'At least one address has an invalid country.'
}, {
    'Id': 'InvalidShowCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The provided ShowCode does not exist'
}, {
    'Id': 'InvalidShowMinDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Start Date cannot be smaller than the 01.01.1900'
}, {
    'Id': 'InvalidShowDateYear',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The end date and the start date must be in the same year'
}, {
    'Id': 'InvalidShowDateDeadLine',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The deadline is expired'
}, {
    'Id': 'InvalidShowDuration',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The show duration is too long'
}, {
    'Id': 'InvalidVenue',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The venue_code is invalid or a venue not authorized for the NF members'
}, {
    'Id': 'PermissionDeniedShowTypeToModify',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The only Standard show  type (CI) is alllowed to modify by the NF members'
}, {
    'Id': 'InvalidStartEventDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The StartEventDate must to be inside the showDate'
}, {
    'Id': 'InvalidEndEventDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The EndEventDate must to be inside the showDate'
}, {
    'Id': 'InvalidIndoorOudoor',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The choice of the Indoor/Outdoor is invalid for this event type'
}, {
    'Id': 'InvalidEventTypeCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'This EventTypeCode does not exist or not permitted.'
}, {
    'Id': 'LockedIsEventApprovedByFEI',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Locked because there is inside the show at the least a event approved by FEI'
}, {
    'Id': 'LockedIsCompetition',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Locked because there is at the least a competition inside a event'
}, {
    'Id': 'PermissionShowEventDenied',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Impossible to modify the show/event for one or more of the following reasons: the show/event was deleted, cancelled, approved by the FEI, contains competitions or the period for modification is expired for that year.'
}, {
    'Id': 'DraftScheduleImportError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Error while importing Draft Schedule document'
}, {
    'Id': 'InvalidEntriesInPrincipleDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid EntriesInPrincipleDate. This date must be less or equal to the event start date.'
}, {
    'Id': 'InvalidNominatedEntriesDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid InvalidNominatedEntriesDate. This date must be less or equal to the event start date.'
}, {
    'Id': 'InvalidDefiniteEntriesDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid InvalidDefiniteEntriesDate. This date must be less or equal to the event start date.'
}, {
    'Id': 'InvalidSubstitutionsLastDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid InvalidSubstitutionsLastDate. This date must be less or equal to the event start date.'
}, {
    'Id': 'InvalidSubstitutionsByOCFirstDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid SubstitutionsByOCFirstDate. This date must be less or equal to the event start date.'
}, {
    'Id': 'InvalidHorseInspectionDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid InvalidHorseInspectionDate. This date must be less or equal to the event start date.'
}, {
    'Id': 'DraftScheduleOnInsert',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "Draft Schedule fields can't be set on creation"
}, {
    'Id': 'InsertAdminLevelError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "Admin Level can't be inserted, this value will be automatically calculated"
}, {
    'Id': 'InsertEntriesInPrincipleDateError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "EntriesInPrincipleDate value can't be set on event creation"
}, {
    'Id': 'InsertNominatedEntriesDateError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "NominatedEntriesDate value can't be set on event creation"
}, {
    'Id': 'InsertDefiniteEntriesDateError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "DefiniteEntriesDate value can't be set on event creation"
}, {
    'Id': 'InsertSubstitutionsLastDateError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "SubstitutionsLastDate value can't be set on event creation"
}, {
    'Id': 'InsertSubstitutionsByOCFirstDateError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "InsertSubstitutionsByOCFirstDateError value can't be set on event creation"
}, {
    'Id': 'InsertHorseInspectionDateError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "HorseInspectionDate value can't be set on event creation"
}, {
    'Id': 'InsertOpenForEntriesError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "OpenForEntries value can't be set on event creation"
}, {
    'Id': 'InvalidAdminLevelFormat',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The AdminLevel format is not valid'
}, {
    'Id': 'PermissionEntriesDatesDenied',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Impossible to modifiy the show/event. You have not sufficient rights to modify Entries Dates.'
}, {
    'Id': 'PermissionOpenEntriesDenied',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Impossible to modifiy the show/event. You have not sufficient rights to modify OpenForEntries'
}, {
    'Id': 'PermissionAdminLevel',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Impossible to modifiy the show/event. You have not sufficient rights to modify AdminLevel.'
}, {
    'Id': 'InvalidCompetitionCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The CompetitionCode is not valid'
}, {
    'Id': 'ResultImportFatal',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Fatal error while importing result data'
}, {
    'Id': 'InvalidEventCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Event Code is not valid'
}, {
    'Id': 'InvalidEventOrCompetitionCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The code provided is not a valid Event Code or a valid Competition Code'
}, {
    'Id': 'NoResult',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'No results in this event'
}, {
    'Id': 'NotImported',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'All results of this event must be imported'
}, {
    'Id': 'LockedByStatus',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'This action is locked by the current result status of the event'
}, {
    'Id': 'InvalidOfficial',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The person is not an official'
}, {
    'Id': 'InvalidOffContactEndDate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The end date cannot be earlier than the start date'
}, {
    'Id': 'InvalidOffContactDisciplineCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The chosen additional role/discipline combination is not valid'
}, {
    'Id': 'InvalidOfficialContactType',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid Official Contact Type'
}, {
    'Id': 'OfficialContactHasNoCertificate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Official Contact has no certificate associated.'
}, {
    'Id': 'InvalidPETStatus',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'There is no accepted PET application for this person'
}, {
    'Id': 'MissingEmailOrNoEmailConfirmationFlag',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The e-mail is Mandatory for an athlete, or the NoEmailConfirmation flag must be set to true'
}, {
    'Id': 'MissingBirthCountryCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The BirthCountryCode is mandatory if the horse has a Passport or a Recognition Card but no breed '
}, {
    'Id': 'MissingColorComplement',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The ColorComplement value is mandatory for this color'
}, {
    'Id': 'MissingConditions',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Conditions parameter is null or empty'
}, {
    'Id': 'MissingDateBirth',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The DateBirth is missing'
}, {
    'Id': 'MissingHorseAnyID',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Horse Any ID is empty or null'
}, {
    'Id': 'MissingHorseDiagram',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'This horse has no diagram'
}, {
    'Id': 'MissingPonyHeight',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Height is mandatory for the Pony'
}, {
    'Id': 'MissingBreed',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Breed is mandatory when the horse has a Passport or a Recognition Card but no country of birth'
}, {
    'Id': 'MissingRecognitionCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The RecognitionCode is required'
}, {
    'Id': 'MissingFEICode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The FEICode is required for horses already having a passport or a recognition card'
}, {
    'Id': 'MissingIssuingBodyCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The IssuingBodyCode is required'
}, {
    'Id': 'MissingPersonAnyID',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Person Any ID is empty or null'
}, {
    'Id': 'MissingCompetingFor',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Competing For is required'
}, {
    'Id': 'MissingEventCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Event Code is empty or null'
}, {
    'Id': 'MissingDisciplineCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Discipline Code is missing'
}, {
    'Id': 'MissingRiderCountryCodeOrOrganizingNFCountryCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Either the "OrganizingNFCountryCode" or the "AthleteCountryCode" fields must be provided'
}, {
    'Id': 'RegistrationTooEarly',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'A registration may not be made more than a few weeks in advance. Currently this is set at 6 weekds, but this is subject to review.'
}, {
    'Id': 'RegistrationTooLate',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The time limit for registration this year is expired.'
}, {
    'Id': 'RegistrationImpossibleButEmailUpdated',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The email was successfully updated but the registration could not made (see other messages).'
}, {
    'Id': 'NoOwner',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The horse does not have an owner'
}, {
    'Id': 'PermissionRequired_NFResult',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The NF Result Admin or NF Result Consult permission is required'
}, {
    'Id': 'NoData',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'There were no Registration records supplied'
}, {
    'Id': 'Locked',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'A field (see description) cannot be modified.'
}, {
    'Id': 'Mandatory',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'A field (see description) is mandatory.'
}, {
    'Id': 'MaxLength',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The field (see description for field name and length) is too long.'
}, {
    'Id': 'BadCriteria',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The search criteria is not recognized or its range is invalid. See detail for the name of the criteria.'
}, {
    'Id': 'BadCode',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': "A field (see description) doesn't contain an recognized value."
}, {
    'Id': 'DownloadLimitReached',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'To much data to download. Please refine your search. See detail for maximum limit.'
}, {
    'Id': 'MissingMandatoryInformation',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Some mandatory information is missing on the record. You have to correct it first.\n    \n    For Horse records, the message is raised either because no owner has been provided or because one or more of the following fields is empty: BirthName, CurrentName, ColorCode, GenderCode, NatPassport, IssuingNFCode. \n    If the horse has a FEI Passport or a Recognition Card then this message is also raised if the Breed or BirthCountryCode field is empty.\n    \n    For Person records, the message is raised when one or more of the following fields is empty: FirstName, FamilyName, NationalityCode, DateOfBirth.'
}, {
    'Id': 'invalidEmailAddress',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Invalid Email Address'
}, {
    'Id': 'InvalidCompetingFor',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The Competing For must be a selected Nationalities'
}, {
    'Id': 'InvalidCompetingForNF',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'The selected CompetingFor does not match an existing NF.'
}, {
    'Id': 'CollectionEmpty',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'the collection is empty'
}, {
    'Id': 'ValidationError',
    'IsCritical': False,
    'IsError': True,
    'IsWarning': False,
    'CEW': 'E',
    'Description': 'Validation error'
}, {
    'Id': 'ListTruncated',
    'IsCritical': False,
    'IsError': False,
    'IsWarning': True,
    'CEW': 'W',
    'Description': 'The returned list was truncated'
}, {
    'Id': 'ResultImportWarning',
    'IsCritical': False,
    'IsError': False,
    'IsWarning': True,
    'CEW': 'W',
    'Description': 'Warning while importing result data'
}, {
    'Id': 'DuplicatedCriteria',
    'IsCritical': False,
    'IsError': False,
    'IsWarning': True,
    'CEW': 'W',
    'Description': 'A criteria is duplicated, only the last given value is used.'
}, {
    'Id': 'NotMapped',
    'IsCritical': False,
    'IsError': False,
    'IsWarning': True,
    'CEW': 'W',
    'Description': 'A field (see description) is not mapped and will be ignored. Do not set this field.'
}, {
    'Id': 'ExportWarning',
    'IsCritical': False,
    'IsError': False,
    'IsWarning': True,
    'CEW': 'W',
    'Description': 'A warning was raised during export. Please see detail for full description.'
}, {
    'Id': 'CriticalException',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'An unexpected error occurred at the server beyond the control of the application. Try again later.'
}, {
    'Id': 'InvalidUser',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'The user is not correct.'
}, {
    'Id': 'UserNotConnected',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'The user is no longer connected. Please connect again'
}, {
    'Id': 'InvalidRoleTypeCode',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'Invalid Role Type'
}, {
    'Id': 'InvalidConnectionTypeCode',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'Invalid connection type code'
}, {
    'Id': 'MissingEmailAddress',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'Missing email address'
}, {
    'Id': 'AccountSuspended',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'AccountSuspended'
}, {
    'Id': 'DBException',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'DB Exception : {0}'
}, {
    'Id': 'DuplicatedRole',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'An identic active role already exists for the invitee.'
}, {
    'Id': 'PersonIsNotOutsider',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'The groups are not those of an outsider.'
}, {
    'Id': 'DuplicatedEmail',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'The email {0} is already in use.'
}, {
    'Id': 'MissingRankingCode',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'Ranking code is mandatory'
}, {
    'Id': 'MissingRankingValidDate',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'Ranking valid date is mandatory'
}, {
    'Id': 'MissingLeagueCode',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'League code is mandatory for this Ranking code'
}, {
    'Id': 'InvalidLeagueCode',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': "This league code doesn't exist or is not suitable for this ranking"
}, {
    'Id': 'InvalidRankingParameter',
    'IsCritical': True,
    'IsError': False,
    'IsWarning': False,
    'CEW': 'C',
    'Description': 'No ranking has found with these parameters'
}]

FEI_MESSAGE_TYPE_DICT = {x['Id']: x for x in FEI_MESSAGE_TYPES}