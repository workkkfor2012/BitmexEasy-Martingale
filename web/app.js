
let $ = id => document.getElementById(id)

$('start').onclick = () => {
    $('start').hidden = true
    pywebview.api.start()
}



python_call_js = {
    on_last_price_update: s => $('last_price').innerHTML = s
}

let i = 1
let a = new WebSocket('ws://127.0.0.1:3000')
a.onmessage = (e) => {
    document.write(e.data)
    if (i < 5) {
        i++
        a.send('aaaaaa' + i)
    }
}
a.onopen = () => {
    a.send('aaaaaa')
}