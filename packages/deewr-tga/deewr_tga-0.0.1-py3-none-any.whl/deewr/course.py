from . import document

class CourseFetcher:

    def __init__(self, client, namespaces, quals, quals_by_unit):
        self.client = client
        self.quals_by_unit = quals_by_unit
        self.quals = quals
        self.namespaces = namespaces

    def fetch_for_code(self, code):
        courseDetails = self.client.service.GetDetails({
            'Code': code
        })

        courseData = {
            'Code': courseDetails.Code,
            'Title': courseDetails.Title,
            'ParentCode': courseDetails.ParentCode,
            'ParentTitle': courseDetails.ParentTitle,
            'ComponentType': courseDetails.ComponentType,
            'ProvidedBy': [],
            'Documents': [],
        }

        if courseDetails.Code in self.quals_by_unit:
            qualCodes = self.quals_by_unit[courseDetails.Code]
            for qualCode in qualCodes:
                if qualCode in self.quals:
                    courseData['ProvidedBy'].append({
                        'Code': self.quals[qualCode]['Code'],
                        'Status': self.quals[qualCode]['Status'],
                        'Title': self.quals[qualCode]['Title']
                    })

        for release in courseDetails.Releases.Release:
            for releaseFile in release.Files.ReleaseFile:
                if ".xml" in releaseFile.RelativePath:
                    url = "{}{}".format("https://training.gov.au/TrainingComponentFiles/", releaseFile.RelativePath.replace("\\","/"))
                    courseData['Documents'].append(document.extract_from_url(self.namespaces, url))


        return courseData