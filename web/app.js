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
        low: $('low').value,
        high: $('high').value,
        targetProfit: $('targetProfit').value,
        priceGap: $('priceGap').value,
        initPos: $('initPos').value,
        API_KEY: $('API_KEY').value,
        API_SECRET: $('API_SECRET').value,
    }

    let s = JSON.stringify(obj)

    localStorage.setItem('s', s)

    ws.send(s)
}

let dic = JSON.parse(localStorage.getItem('s'))
$('low').value = dic.low
$('high').value = dic.high
$('targetProfit').value = dic.targetProfit
$('priceGap').value = dic.priceGap
$('initPos').value = dic.initPos
$('API_KEY').value = dic.API_KEY
$('API_SECRET').value = dic.API_SECRET