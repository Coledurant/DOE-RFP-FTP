class ConEdisonRFP(object):

    all_rfps = []

    def __init__(self, project_name, current_status, documents = []):

        self.project_name = project_name
        self.current_status = current_status
        self.documents = documents

        ConEdisonRFP.all_rfps.append(self)

    def __str__(self):

        return self.project_name

class ConEdisonDocument(object):

    all_documents = []

    def __init__(self, document_name, url):

        self.document_name = document_name
        self.url = url

        ConEdisonDocument.all_documents.append(self)

    def __str__(self):

        return self.document_name

class DominionRSSItem(object):

    def __init__(self, title, link, description):

        self.title = title
        self.link = link
        self.description = description
