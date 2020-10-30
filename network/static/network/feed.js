
function edit(id, content) {
    console.log("prepared post " +  id + " for edit");
    document.querySelector('#post' + id).innerHTML = "<textarea id='content" + id + "'>" + content + "</textarea>" +
    "<br><small><a href='#' onclick='update(" + id + ");' > Save </a></small> | " +
    "<small><a href='#' onclick='cancel(" + id + ");' > Cancel </a></small>"
}

function cancel(id) {

}

function update(id) {

    content = document.querySelector("#content" + id).value
    
    fetch('/post/' + id, {
        method: 'POST',
        body: JSON.stringify({
            id: id,
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.status);


        document.querySelector("#post" + result.id).innerHTML = result.content + 
        "<br>" +
        "<small><i>" + result.updated + "</i></small>" +
        "<small><a href='#' onclick='edit(" + result.id + ", \"" + result.content + "\");'> Edit</a></small>"
    }); 

    return false
}