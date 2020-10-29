
function edit(id, content) {
    console.log("prepared post " +  id + " for edit");
    document.querySelector('#post' + id).innerHTML = "<textarea>" + content + "</textarea>";
}

function update() {

    content = document.querySelector("#post-content").value 
    post_id = document.querySelector("#post_id").value 
    fetch('post', {
        method: 'PUT',
        body: JSON.stringify({
            id: post_id,
            content: content
        })
    });
}