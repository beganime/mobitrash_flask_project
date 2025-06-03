    var menu = document.getElementById("menu")
    var menubtn = document.getElementById("menubtn")
    var headhome = document.getElementById("headhome")
    var profilebtn = document.getElementById("profilebtn")
    var profiletext = document.getElementById("profiletext")
    var mobsamsung = document.getElementById("mobsamsung")
    var tabsamsung = document.getElementById("tabsamsung")
    var comsamsung = document.getElementById("comsamsung")
    var mobapple = document.getElementById("mobapple")
    var tabapple = document.getElementById("tabapple")
    var comapple = document.getElementById("comapple")
    var mobileP = document.getElementById("mobileP")
    var tabletP = document.getElementById("tabletP")
    var computersP = document.getElementById("computersP")
    mobileP.addEventListener('click', function() {
        if (mobsamsung.style.display == "none") {
            mobsamsung.style.display = "block"
            mobapple.style.display = "block"
        } else {
            mobsamsung.style.display = "none"
            mobapple.style.display = "none"
        }
    })
    tabletP.addEventListener('click', function() {
        if (tabsamsung.style.display == "none") {
            tabsamsung.style.display = "block"
            tabapple.style.display = "block"
        } else {
            tabsamsung.style.display = "none"
            tabapple.style.display = "none"
        }
    })
    computersP.addEventListener('click', function() {
        if (comsamsung.style.display == "none") {
            comsamsung.style.display = "block"
            comapple.style.display = "block"
        } else {
            comsamsung.style.display = "none"
            comapple.style.display = "none"
        }
    })
    var message = document.getElementById("message").textContent
    var page = document.getElementById("page").textContent
    var p1 = document.getElementById("p1")
    var p2 = document.getElementById("p2")
    var p3 = document.getElementById("p3")
    var p4 = document.getElementById("p4")
    var p146 = document.getElementById("p146")
    const body = document.getElementById("body")
    const error = document.getElementById("error")
    const category_samsung_mobile = document.getElementById("category_samsung_mobile")
    const category_samsung_tablet = document.getElementById("category_samsung_tablet")
    const category_samsung_notebook = document.getElementById("category_samsung_notebook")
    const category_apple_mobile = document.getElementById("category_apple_mobile")
    const category_apple_tablet = document.getElementById("category_apple_tablet")
    const category_apple_notebook = document.getElementById("category_apple_notebook")

    const samsung_phone_addnew = document.getElementById("samsung_phone_addnew")
    const samsung_tablet_addnew = document.getElementById("samsung_tablet_addnew")
    const samsung_notebook_addnew = document.getElementById("samsung_notebook_addnew")

    console.log("сообщение от сервера открыть", message)

    if (message == "home") {
        console.log(message)
        body.style.display = "block"
        category_samsung_mobile.style.display = "none"
    }
    if (message == "samsung_phone") {
        console.log(message)
        headhome.style.borderBottom = "0"
        headhome.addEventListener('mouseenter', function() {
            headhome.style.borderBottom = "5px solid #DC7000"
        })
        headhome.addEventListener('mouseleave', function() {
            headhome.style.borderBottom = "0"
        })
        menubtn.innerHTML = "mobiles / samsung"
        menubtn.style.borderBottom = "5px solid #DC7000"
        body.style.display = "none"
        category_samsung_mobile.style.display = "flex"
        if (page == "1") {
            p1.style.color = "red"
        } else if (page == "2") {
            p2.style.color = "red"
        } else if (page == "3") {
            p3.style.color = "red"
        } else if (page == "4") {
            p4.style.color = "red"
        }
    }
    if (message == "apple_phone") {
        console.log(message)
        headhome.style.borderBottom = "0"
        headhome.addEventListener('mouseenter', function() {
            headhome.style.borderBottom = "5px solid #DC7000"
        })
        headhome.addEventListener('mouseleave', function() {
            headhome.style.borderBottom = "0"
        })
        menubtn.innerHTML = "mobiles / apple"
        menubtn.style.borderBottom = "5px solid #DC7000"
        body.style.display = "none"
        category_apple_mobile.style.display = "flex"
    }
    if (message == "samsung_tablet") {
        console.log(message)
        headhome.style.borderBottom = "0"
        headhome.addEventListener('mouseenter', function() {
            headhome.style.borderBottom = "5px solid #DC7000"
        })
        headhome.addEventListener('mouseleave', function() {
            headhome.style.borderBottom = "0"
        })
        menubtn.innerHTML = "tablets / samsung"
        menubtn.style.borderBottom = "5px solid #DC7000"
        body.style.display = "none"
        category_samsung_tablet.style.display = "flex"
    }
    if (message == "apple_tablet") {
        console.log(message)
        headhome.style.borderBottom = "0"
        headhome.addEventListener('mouseenter', function() {
            headhome.style.borderBottom = "5px solid #DC7000"
        })
        headhome.addEventListener('mouseleave', function() {
            headhome.style.borderBottom = "0"
        })
        menubtn.innerHTML = "tablets / apple"
        menubtn.style.borderBottom = "5px solid #DC7000"
        body.style.display = "none"
        category_apple_tablet.style.display = "flex"
    }
    if (message == "samsung_notebook") {
        console.log(message)
        headhome.style.borderBottom = "0"
        headhome.addEventListener('mouseenter', function() {
            headhome.style.borderBottom = "5px solid #DC7000"
        })
        headhome.addEventListener('mouseleave', function() {
            headhome.style.borderBottom = "0"
        })
        menubtn.innerHTML = "Computers / samsung"
        menubtn.style.borderBottom = "5px solid #DC7000"
        body.style.display = "none"
        category_samsung_notebook.style.display = "flex"
    }
    if (message == "apple_notebook") {
        console.log(message)
        headhome.style.borderBottom = "0"
        headhome.addEventListener('mouseenter', function() {
            headhome.style.borderBottom = "5px solid #DC7000"
        })
        headhome.addEventListener('mouseleave', function() {
            headhome.style.borderBottom = "0"
        })
        menubtn.innerHTML = "Computers / apple"
        menubtn.style.borderBottom = "5px solid #DC7000"
        body.style.display = "none"
        category_apple_notebook.style.display = "flex"
    }
    if (message == "add_samsung_phone") {
        body.style.display = "none"
        samsung_phone_addnew.style.display = "flex"
    }
    if (message == "add_samsung_tablet") {
        body.style.display = "none"
        samsung_tablet_addnew.style.display = "flex"
    }
    if (message == "add_samsung_notebook") {
        body.style.display = "none"
        samsung_notebook_addnew.style.display = "flex"
    }
    if (message == "user") {
        body.style.display = "none"
        error.style.display = "flex"
    }

    const scrollToTop = document.getElementById("scrollToTop")
    window.onscroll = function() {
        scrollFunc()
    }

    function scrollFunc() {
        if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
            scrollToTop.style.display = "block"
        } else {
            scrollToTop.style.display = "none"
        }
    }
    scrollToTop.addEventListener("click", function() {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        })
    })
    menubtn.addEventListener('click', function() {
        menu.classList.toggle('open');
    });
    setTimeout(() => {
        const cookieUsername = getCookie('username')
        if (cookieUsername) {
            if (cookieUsername == "none") {
                console.log("username не найден")
            } else {
                console.log('Значение куки "username":', cookieUsername)
                profiletext.innerHTML = "Profile " + cookieUsername[0]
                profilebtn.style.display = "block"
                logbtn.style.display = "none"
            }
        } else {
            console.log('Куки "username" не найдена.')
        }
    }, 1000);

    function getCookie(key) {
        const name = key + "="
        const decodedCookie = decodeURIComponent(document.cookie)
        const ca = decodedCookie.split(';')
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i]
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length)
            }
        }
        return null
    }

    function openProfile() {
        const cookieUsername = getCookie('username')
        const response = window.location.href = `/profile/${cookieUsername}`
        return response
    }
    var chinput = document.getElementById("chinput")
    var cheinput = document.getElementById("cheinput")
    if (chinput) {
        chinput.addEventListener('click', function() {
            if (cheinput.style.display == "none") {
                cheinput.style.display = "block"
                chinput.style.color = "#ffffff"
            } else {
                cheinput.style.display = "none"
                chinput.style.color = "#dcdcdcb5"
            }
        })
    }
    const mobile_update = document.getElementById("mobile_update")
    const addsamsungphone = document.getElementById("addsamsungphone")
    const mobile_in_db = document.getElementById("mobile_in_db")
    const charact = document.getElementById("charact")

    function mobile_added_info() {
        console.log("add")

    }
    if (message == "mobile_added") {
        body.style.display = "none"
        mobile_update.style.display = "grid"
        samsung_phone_addnew.style.display = "flex"
        addsamsungphone.style.display = "none"
        console.log("info")
    }
    if (message == "mobile_in_db") {
        body.style.display = "none"
        mobile_update.style.display = "grid"
        samsung_phone_addnew.style.display = "flex"
        charact.style.display = "none"
        addsamsungphone.style.display = "none"
        console.log("mobile is added dawno")
    }