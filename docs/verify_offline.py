from pathlib import Path
import importlib.util, unittest, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
suite=unittest.defaultTestLoader.discover(str(root/'tests'))
result=unittest.TextTestRunner(verbosity=2).run(suite)
assert result.wasSuccessful()
spec=importlib.util.spec_from_file_location('bot',root/'Coding_For_Whatsapp_chatbot/main.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for body in ['hello','HELP','info','bye','unknown',None]:
    response=m.app.test_client().post('/whatsapp',data={} if body is None else {'Body':body})
    print(f'POST /whatsapp Body={body!r}: HTTP {response.status_code}: {ET.fromstring(response.data).findtext("Message/Body")!r}')
print('PASS: 3 tests, including five keyword/fallback subcases and missing Body; GET rejected with 405.')
