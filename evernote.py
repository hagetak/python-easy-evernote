class Evernote:

    def __init__(self, token):

        self.client = EvernoteClient(token=token, sandbox=False)
        self.resources = []
        self.attachment_contents = ''

    def build_content(self, base_content):
        content = '<?xml version="1.0" encoding="UTF-8"?>'
        content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        content += "<en-note>%s<br/>%s</en-note>" % (base_content, self.attachment_contents)
        return content

    def create_note_book(self, title, content, note_book_gid=""):
        note = Types.Note()
        note.title = title
        note.content = self.build_content(content)
        note.resources = self.resources
        if len(note_book_gid) > 0:
            note.notebookGuid = note_book_gid

        note_store = self.client.get_note_store()
        created_note = note_store.createNote(note)
        return created_note

    def add_resources(self, image_url):
        bodybinary = open(image_url, 'rb').read()
        bodyhash = hashlib.md5(bodybinary).hexdigest()
        self.attachment_contents += '<br /><en-media type="%s" hash="%s" />' % ('image/png', bodyhash)

        data = Types.Data()
        data.size = len(bodybinary)
        data.bodyHash = bodyhash
        data.body = b64decode(str(base64.b64encode(bodybinary).decode()))
        resource = Types.Resource()
        resource.mime = 'image/png'
        resource.data = data
        self.resources.append(resource)
