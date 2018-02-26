let $ = id => document.getElementById(id)
let start = $('start')
let status = $('status')
let config = $('config')

let ws = new WebSocket('ws://127.0.0.1:3000')

ws.onmessage = (e) => {
    start.hidden = true
    status.innerText = e.data
}

start.onclick = () => {
    let obj = {
        supportPrice: $('supportPrice').value,
        pressurePrice: $('pressurePrice').value,
        targetPrice: $('targetPrice').value,
        priceGap: $('priceGap').value,
        initPos: $('initPos').value,
        API_KEY: $('API_KEY').value,
        API_SECRET: $('API_SECRET').value,
    }
    let s = JSON.stringify(obj)
    console.log(s)
    ws.send(s)
}

