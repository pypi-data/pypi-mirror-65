import json


def cache_qualifications(client, qualificationsJsonFilePath, qualificationsIndexedByUnitPath):
    # Fetch all classifications
    qualifications = {}
    qualificationsIndexedByUnitType = {}
    page = 0
    while True:
        page = page + 1

        print(page)

        results = client.service.Search({
            'PageNumber': page,
            'PageSize': 20,
            'TrainingComponentTypes': {
                'IncludeAccreditedCourse': False,
                'IncludeAccreditedCourseModule': False,
                'IncludeQualification': True,
                'IncludeSkillSet': False,
                'IncludeTrainingPackage': False,
                'IncludeUnit': False,
                'IncludeContextualisation': True,
            },
        })

        if 'Results' not in results:
            break

        if results['Results'] is None:
            break

        if 'TrainingComponentSummary' not in results['Results']:
            break

        if results['Results']['TrainingComponentSummary'] is None:
            break

        if len(results['Results']['TrainingComponentSummary']) == 0:
            break

        for qualificationResult in results['Results']['TrainingComponentSummary']:
            qualificationDetails = client.service.GetDetails({
                'Code': qualificationResult['Code'],
                'IncludeLegacyData': True,
                'InformationRequest': {
                    'ShowAttachments': False,
                    'ShowClassifications': False,
                    'ShowCompanionVolumeLinks': False,
                    'ShowCompletionMapping': False,
                    'ShowComponents': False,
                    'ShowContacts': False,
                    'ShowCurrencyPeriods': False,
                    'ShowDataManagers': False,
                    'ShowFiles': False,
                    'ShowIndustrySectors': False,
                    'ShowMappingInformation': False,
                    'ShowOccupations': False,
                    'ShowRecognitionManagers': False,
                    'ShowReleases': True,
                    'ShowUnitGrid': True,
                    'ShowUsageRecommendation': False,
                }
            })

            qualification = {
                'Code': qualificationResult.Code,
                'Status': qualificationResult.CurrencyStatus,
                'Title': qualificationResult.Title,
                'Units': [],
            }

            if "Releases" in qualificationDetails:
                if "Release" in qualificationDetails["Releases"]:
                    for release in qualificationDetails['Releases']['Release']:
                        if 'UnitGrid' in release and release['UnitGrid'] is not None:
                            if 'UnitGridEntry' in release['UnitGrid']:
                                for entry in release['UnitGrid']['UnitGridEntry']:
                                    qualification['Units'].append({
                                        'Code': entry['Code'],
                                        'IsEssential': entry['IsEssential'],
                                        'Title': entry['Title'],
                                    })

                                    if entry['Code'] not in qualificationsIndexedByUnitType:
                                        qualificationsIndexedByUnitType[entry['Code']] = []

                                    qualificationsIndexedByUnitType[entry['Code']].append(qualificationResult.Code)

            qualifications[qualificationResult['Code']] = qualification

    print('Writing JSON')

    f = open(qualificationsJsonFilePath, "w")
    json.dump(qualifications, f, indent=4)
    f.close()

    f = open(qualificationsIndexedByUnitPath, "w")
    json.dump(qualificationsIndexedByUnitType, f, indent=4)
    f.close()