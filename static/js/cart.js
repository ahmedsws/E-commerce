

var updatebtn = document.getElementsByClassName('update-cart'); 

for (i = 0 ; i < updatebtn.length ; i++) {
    updatebtn[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('product_id: ',productId , 'action: ',action ,'user is : ' , user)
        if (user == 'AnonymousUser') 
        {
            console.log('go to login page');
        }
        else
        {
            updateUserOrder(productId,action)
        }
    });

    function updateUserOrder(productId , action) {
        var url = '/update_item/'
        fetch(url, {
            method : 'POST',
            headers : {
                'Content_Type' : 'application/json',
                'X-CSRFToken' : csrftoken
            },
            body : JSON.stringify({'productId': productId, 'action' : action})
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data',data)
            location.reload()
        })
    }
    
}