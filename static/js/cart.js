var updateBtns = document.getElementsByClassName('update-cart')

for (i =0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        if (user === 'AnonymousUser'){
            console.log('Not logged in')
     }
        else {
              updateUserOrder(productId,action)
     }
   })
}

function updateUserOrder(productId,action){
    console.log('User: ', user, 'is logged in..sendind data...')
    var url = '/update_item/'
    
    fetch(url, {
        method: 'POST',
        headers : {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then ((response) => {
        return response.json();
})
    .then((data) => {
       console.log('Data: ', data)
       location.reload()
    });
}