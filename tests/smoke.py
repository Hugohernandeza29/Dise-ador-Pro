from pathlib import Path
import json
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
 page.wait_for_function('doc.layers.length === 4')
 page.locator('#text').click()
 page.locator('#content').fill('Prueba Banco Amazonas')
 page.locator('#content').dispatch_event('change')
 page.locator('#x').fill('150');page.locator('#x').dispatch_event('change')
 assert page.evaluate('active().x')==150
 # Move selected layer using actual pointer events on canvas.
 r=page.locator('#canvas').bounding_box()
 px=r['x']+170*r['width']/1080;py=r['y']+120*r['height']/1350
 page.mouse.move(px,py);page.mouse.down();page.mouse.move(px+20,py+20);page.mouse.up()
 assert page.evaluate('active().x')>150
 page.locator('.layer.active button[title="Bloquear o desbloquear"]').click()
 assert page.locator('#content').is_disabled()
 page.locator('.layer.active button[title="Bloquear o desbloquear"]').click()
 assert page.locator('#content').is_enabled()
 page.locator('.layer.active button[title="Mostrar u ocultar"]').click()
 assert page.evaluate('active().hidden')
 page.locator('.layer.active button[title="Mostrar u ocultar"]').click()
 page.locator('#duplicate').click()
 assert page.evaluate('doc.layers.length')==6
 page.locator('#delete').click()
 assert page.evaluate('doc.layers.length')==5
 page.locator('#undo').click()
 page.wait_for_function('doc.layers.length === 6')
 page.locator('#redo').click()
 page.wait_for_function('doc.layers.length === 5')
 with page.expect_download() as info:page.locator('#save').click()
 project=Path('/tmp/designer-test.json');info.value.save_as(project)
 data=json.loads(project.read_text());assert data['layers'][-1]['text']=='Prueba Banco Amazonas'
 page.locator('#projectFile').set_input_files(str(project))
 page.wait_for_function("document.getElementById('status').textContent.includes('Proyecto abierto')")
 # Import a real PNG and retain image bytes through save/reopen.
 page.screenshot(path='/tmp/import-test.png')
 page.locator('#imageFile').set_input_files('/tmp/import-test.png')
 page.wait_for_function("doc.layers.at(-1).type === 'image'")
 assert page.evaluate('active().ratio')
 old=page.evaluate('active().h/active().w')
 page.locator('#w').fill('400');page.locator('#w').dispatch_event('change')
 assert abs(page.evaluate('active().h/active().w')-old)<.01
 with page.expect_download() as info:page.locator('#export').click()
 info.value.save_as('/tmp/designer-export.png')
 assert Path('/tmp/designer-export.png').read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
 page.locator('#exportType').select_option('JPG')
 with page.expect_download() as info:page.locator('#export').click()
 info.value.save_as('/tmp/designer-export.jpg')
 assert Path('/tmp/designer-export.jpg').read_bytes()[:2]==b'\xff\xd8'
 # Persistence after reload.
 page.reload();page.wait_for_function('doc.layers.length === 6 && images.size === 1')
 page.screenshot(path='/tmp/disenador-pro-desktop.png',full_page=True)
 page.set_viewport_size({'width':390,'height':844})
 page.screenshot(path='/tmp/disenador-pro-mobile.png',full_page=True)
 assert not errors,errors
 print('PASS: text edit, position, duplicate/delete, undo/redo, project roundtrip, image import, aspect ratio, PNG/JPG export, reload persistence, mobile render; no browser errors.')
 browser.close()
