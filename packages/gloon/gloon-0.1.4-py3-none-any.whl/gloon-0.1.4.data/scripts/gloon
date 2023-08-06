import os
import tempfile
import datetime
import sys
import re
import zeep
import subprocess
from halo import Halo
from PyInquirer import style_from_dict, Token, prompt, Separator

if __name__ == "__main__":
    try:
        spinner = Halo(
            text='Conectando con tu cuenta de Netsuite', 
            text_color="magenta",
            spinner={
                "interval": 40,
                "frames": [
                    "⣾",
                    "⣽",
                    "⣻",
                    "⢿",
                    "⡿",
                    "⣟",
                    "⣯",
                    "⣷"
                ]
            }
        )
        #current working directory
        cwd = os.getcwd()
        #sdf file for get account credentials
        sdf = open(os.path.join(cwd,'.sdf'), 'r+' ) if os.path.isfile(os.path.join(cwd,'.sdf')) == True else None
        #local file name passed from argument
        localfile = sys.argv[1] if len(sys.argv) > 1 else None
        name = localfile.split('\\')[-1]
        if localfile is not None and sdf is not None:
            #start spinner animation
            spinner.start()
            
            lines = sdf.readlines()

            sdf.close()
            passport = dict([(item.split('=')[0], item.split('=')[1].replace('\n','')) for item in lines])
            
            client = zeep.Client('https://tstdrv1989308.suitetalk.api.netsuite.com/wsdl/v2014_2_0/netsuite.wsdl')
            Passport = client.get_type('ns0:Passport')
            credentials = Passport(email=passport['email'],password=passport['pass'],account=passport['account'], role=passport['role'])
            
            try:
                login = client.service.login(passport=credentials)
                if login.status.isSuccess:

                    FileSearch = client.get_type('ns11:FileSearch')
                    FileSearchBasic = client.get_type('ns5:FileSearchBasic')
                    SearchStringField = client.get_type('ns0:SearchStringField')
                    Record = client.get_type('ns0:RecordRef')

                    filesearch = FileSearch(basic=FileSearchBasic(name=SearchStringField(searchValue=name, operator='is')))

                    search = client.service.search(searchRecord=filesearch)
                    if search.body.searchResult.status.isSuccess:
                        record = search.body.searchResult.recordList
                        if record is not None:
                            spinner.succeed()
                            questions = [
                                {
                                    'type': 'list',
                                    'name': 'file',
                                    'qmark': '!',
                                    'message': 'He econtrado estos archivos que coinciden con tu búsqueda:',
                                    'choices': ["[{internalid}] {parent}/{file}".format(internalid= file.internalId, parent= file.folder.name.replace(' : ','/'), file=file.name) for file in record.record]
                                }
                            ]
                            answers = prompt(questions)
                            internalid = re.findall(r'\-?\d{1,}',answers['file'])

                            remotefile = client.service.get(baseRef=Record(name=name, internalId=internalid[0], type='file'))
                            with open(os.path.join(tempfile.gettempdir(),name),'wb+') as  file:
                                file.write(remotefile.body.readResponse.record.content)
                            file.close()
                            subprocess.call(['code','--diff', localfile , os.path.join(tempfile.gettempdir(),name)] ,shell=True)
                        else:
                            spinner.warn('No se encontraron coincidencias :/')
                else:
                    spinner.warn("gloon no ha podido conectarse a tu cuenta de Netsuite :(")
            except zeep.exceptions.Fault as error:
                spinner.fail('{} :('.format(error.message))
        else:
            spinner.warn('gloon necesita un archivo .sdf y el nombre del archivo a buscar en Netsuite :/')
    except (KeyboardInterrupt):
        exit();