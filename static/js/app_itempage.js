const burger = document.querySelector('.burger2')
const menu = document.querySelector('.menu')
const dropdown = document.querySelector('.dropdown')
const list = document.querySelector('.list')
burger.addEventListener('click', function () {
    burger.classList.toggle('toggle');
    burger.classList.toggle('hiburger');
    menu.classList.toggle('closemenu')
});
const accounts = document.querySelector('.accounts')
accounts.addEventListener('click', function () {
    dropdown.classList.toggle('comedown')
    list.classList.toggle('addcolor')
})