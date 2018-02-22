
let $ = id => document.getElementById(id)

$('start').onclick = () => {
    $('start').hidden = true
    pywebview.api.start()
}



python_call_js = {
    on_last_price_update: s => $('last_price').innerHTML = s
}
