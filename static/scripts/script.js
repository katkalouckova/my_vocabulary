let items = document.querySelectorAll("input[type='checkbox']");
let selected = true;

function toggle(event) {
    for (let i = 0; i < items.length; i++) {
        if (items[i].type == "checkbox") {
            items[i].checked = selected;
        }
    }
    selected = !selected;
}