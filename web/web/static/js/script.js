function insertBold(str, pos, len) {
    return str.slice(0, pos) + "<strong>" + str.slice(pos, pos + len) + "</strong>" + str.slice(pos + len);
}

document.querySelector('#elastic').oninput = function () {
    let val = this.value.trim();
    let projects = document.querySelectorAll('.elastic li');
    console.log("116");
    if (val != '') {
        projects.forEach(function (elem) {
            if (elem.innerText.search(val) == -1) {
                elem.classList.add('hide');
                elem.innerHTML = elem.innerText;
            }
            else {
                elem.classList.remove('hide');
                elem.innerHTML = insertBold(elem.innerText, elem.innerText.search(val), val.length);
            }
        });
    }
    else {
        projects.forEach(function (elem) {
            elem.classList.remove('hide');
            elem.innerHTML = elem.innerText;
        });
    }
}