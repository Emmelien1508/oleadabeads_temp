$(document).ready(function() {
    const hamburgerBtn = document.querySelector('.hamburger-button')
    const pageWrapper = document.querySelector('.body-wrapper')
    const sidebarBox = document.querySelector('.box')
    const darkScreen = document.querySelector('.dark-screen')
    const stickyTop = document.querySelector('.sticky-top')

    $( '.hamburger-button' ).on('click', function (e) {        
        console.log(hamburgerBtn)
        console.log(sidebarBox)
        hamburgerBtn.classList.toggle('active');
        sidebarBox.classList.toggle('active');
        darkScreen.classList.toggle('covering');
        stickyTop.classList.toggle('covering');
    })
})

