# Tweeter
Twitter-like social network website for making posts and following users.

# Specification
Using Python, JavaScript, HTML, and CSS, complete the implementation of a social network that allows users to make posts, follow other users, and “like” posts. You must fulfill the following requirements:

## New Post: 

Users who are signed in are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

## All Posts: 

The “All Posts” link in the navigation bar takes the user to a page where they can see all posts from all users, with the most recent posts first.

Each post  includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has (this will be 0 for all posts initially)

## Profile Page: 

Clicking on a username loads that user’s profile page. This page displays:
    - Display the number of followers the user has, as well as the number of people that the user follows.
    - Display all of the posts for that user, in reverse chronological order.
    - For any other user who is signed in, this page also displays a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user is not be able to follow themselves.

## Following: 

The “Following” link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
This page behaves just as the “All Posts” page does, just with a more limited set of posts.
This page is only available to users who are signed in.

## Pagination: 

On any page that displays posts, posts only displays 10 on a page. If there are more than ten posts, a “Next” button appears to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button appears to take the user to the previous page of posts as well.

## Edit Post: 

Users is able to click an “Edit” button or link on any of their own posts to edit that post.
When a user clicks “Edit” for one of their own posts, the content of their post is replaced with a textarea where the user can edit the content of their post.
The user then can click on “Save” to update the edited post. Using JavaScript, this is achieved without requiring a reload of the entire page.
For security, the application is designed such that it is not possible for a user, via any route, to edit another user’s posts.

## “Like” and “Unlike”: 

Users can click a link on any post to toggle whether or not they “like” that post.
Using JavaScript, this happens asynchronously and the server knows to update the like count (as via a call to fetch) and then update the post’s like count displayed on the page, without requiring a reload of the entire page.
