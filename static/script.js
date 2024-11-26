const menuMobie = document.querySelector('.menu-mobile');
const body = document.querySelector('body');
const itemsAnimate = document.querySelectorAll('[data-animate]');
const navItem = document.querySelectorAll('.nav-item');

const idnavItens = []
document.querySelectorAll('.nav-item a').forEach(i => { idnavItens.push(i.hash) });

const sectionNavItens = document.querySelectorAll(idnavItens)

menuMobie.addEventListener('click', () => {
    menuMobie.classList.toggle('bi-x');
    body.classList.toggle('menu-nav-active')
})


navItem.forEach(item => {
    item.addEventListener('click', () => {
        if (body.classList.contains('menu-nav-active')) {
            body.classList.remove('menu-nav-active');
            menuMobie.classList.toggle('bi-x')
        }
    })
})

function activeClassNav() {
    const windowTop = window.scrollY + window.innerHeight * 0.40
    for (let i = 0; i < sectionNavItens.length; i += 1) {
        if (i < sectionNavItens.length - 1) {
            if (windowTop > sectionNavItens[i].offsetTop && windowTop < sectionNavItens[i + 1].offsetTop) {
                document.querySelector(`[data-href="#${sectionNavItens[i].id}"]`).classList.add('active')
            } else {
                document.querySelector(`[data-href="#${sectionNavItens[i].id}"]`).classList.remove('active')
            } 
        } else {
            if (windowTop > sectionNavItens[i].offsetTop) {
                document.querySelector(`[data-href="#${sectionNavItens[i].id}"]`).classList.add('active')
            } else {
                document.querySelector(`[data-href="#${sectionNavItens[i].id}"]`).classList.remove('active')
            } 
        }

    }
}


//Animação
function animeScroll() {
    const windowTop = window.scrollY + window.innerHeight * 0.85
    itemsAnimate.forEach(e => {
        if (windowTop > e.offsetTop) {
            e.classList.add('animate');
        } else {
            e.classList.remove('animate');
        }
    })
}

async function sendEmail(event) {
    event.preventDefault();
    const csrfToken = document.querySelector('[name="csrf_token"]').value;
    const name = document.querySelector('#contato-email [name="nome"]').value;
    const email = document.querySelector('#contato-email [name="email"]').value;
    const msg = document.querySelector('#contato-email [name="mensagem"]').value;

    const btnSend = document.querySelector('#btn-contato-enviar');
    const btnLoading = document.querySelector('#btn-contato-loading');
    const alertSuccess = document.querySelector('#alert-contato-success');
    const alertError = document.querySelector('#alert-contato-error');

    const changeBtnLoading =(showSend) => {
        btnSend.style.display = showSend? 'block': 'none';
        btnLoading.style.display = showSend? 'none': 'block';
    }

    changeBtnLoading(false);

    try {
        let response = await fetch('/send', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body:JSON.stringify({
                name: name,
                email: email,
                msg: msg
            })

        });
        let data = await response.json();

        if (data['msg']){
            alertSuccess.style.display = 'block';
        } else {
            console.log('asdas')
            alertError.style.display = 'block';
        }

    } catch (error) {
        alertError.style.display = 'block';
    } finally {
        changeBtnLoading(true);
        setTimeout(() =>{
            alertError.style.display = 'none';
            alertSuccess.style.display = 'none';
        }, 5000)
    }
}


activeClassNav();
animeScroll();
window.addEventListener('scroll', () => {
    animeScroll();
    activeClassNav();
})

