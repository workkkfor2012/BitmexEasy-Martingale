let $ = id => document.getElementById(id)
let start = $('start')
let status = $('status')
let config = $('config')

let ws = new WebSocket('ws://127.0.0.1:3000')

ws.onmessage = (e) => {
    start.hidden = true
    status.innerText = e.data
}

start.onclick = () =>
    ws.send(config.innerText)

