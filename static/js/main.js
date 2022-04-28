console.log(user);

let add_cart = document.getElementsByClassName("add-cart");

for (var i = 0; i < add_cart.length; i++) {
  add_cart[i].addEventListener("click", function (e) {
    e.preventDefault();
    product = this.dataset.product;
    action = this.dataset.action;

    if (user == "AnonymousUser") {
      console.log("please log in ");
    } else {
      // console.log("user sending the data");
      updateorder(product, action);
    }
  });
}

function updateorder(product, action) {
  var url = "/update-item/";

  body_data = { product: product, action: action };
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(body_data),
  })
    .then((response) => {
      return response.json();
    })

    .then((data) => {
      console.log("data : ", data);
      location.reload();
    });
}

let delete_order = document.getElementsByClassName("delete-order");

for (var i = 0; i < delete_order.length; i++) {
  delete_order[i].addEventListener("click", function () {
    var delete_orderitem = this.dataset.delete;
    var product_id = this.dataset.product;
    if (user == "AnonymousUser") {
      console.log("please log in ");
    } else {
      delete_orderitems(delete_orderitem, product_id);
    }
  });
}

function delete_orderitems(delete_orderitem, product_id) {
  var url = "/delete-item/";

  body_data = { delete_item: delete_orderitem, product_id: product_id };
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(body_data),
  })
    .then((response) => {
      return response.json();
    })

    .then((data) => {
      console.log("data : ", data);
      location.reload();
    });
}
