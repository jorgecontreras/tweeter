
function edit(id, content) {
    console.log("prepared post " +  id + " for edit");
    document.querySelector('#post' + id).innerHTML = "<textarea id='content" + id + "'>" + content + "</textarea>" +
    "<br><small><a href='#a' onclick='update(" + id + ");' > Save </a></small> | " 
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

        
        updated_content = result.content + 
        "<br>" +
        "<small><i>" + result.updated + "</i></small>" +
        "<small><a href='#a' onclick='edit(" + result.id + ", \"" + result.content + "\");'> Edit </a></small>" +
        "<small><a href='#a' onclick='like(" + id + ");' id='like_post" + id + "'>"

        if (result.liked) {
            updated_content += "<img src='/static/network/like.png' height='20px' %}>"
        } else {
            updated_content += "<img src='/static/network/unlike.png' height='20px' %}>"
        }
        
        updated_content += "</a></small>"

        document.querySelector("#post" + result.id).innerHTML = updated_content
                
    }); 

    return false
}

function follow(profile_id) {
    fetch('/follow/' + profile_id, {
        method: "POST", 
        body: JSON.stringify({
            profile_id: profile_id
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.status);
        console.log(result.user_following);

        if (result.user_following) {
            document.querySelector("#follow_button").innerHTML = "Unfollow"
        } else {
            document.querySelector("#follow_button").innerHTML = "Follow"
        }

        document.querySelector("#followers").innerHTML = result.followers
        
    });

    return false
}

function like(post_id) {

    fetch('/like/' + post_id, {
        method: "POST",
        body: ""
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.liked);
        if(result.liked) {
            document.querySelector("#like_post"+post_id).innerHTML = "<img src='/static/network/like.png' height='20px' %}'>"
        } else {
            document.querySelector("#like_post"+post_id).innerHTML = "<img src='/static/network/unlike.png' height='20px' %}'>"
        }

        document.querySelector("#like_count"+post_id).innerHTML = result.total_likes
    })
    
    return false
}