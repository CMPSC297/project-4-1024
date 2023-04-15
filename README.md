# project-4-1024
project-4-1024 created by GitHub Classroom

index.html:
This is a Django template file that generates HTML code for the "All Posts" page of a social network web application. The page displays a list of posts made by users, and allows logged-in users to create new posts and edit their own posts.

The template extends a base layout file and includes a block named "scripts", which includes a JavaScript file called "main.js" that provides client-side functionality for the page. The block named "body" defines the main content of the page.

The page starts with a form that allows users to create new posts. The form is generated using a Django form object named "form". If the user is not anonymous, the form is displayed along with a submit button. Otherwise, only the posts are displayed.

The list of posts is generated using a loop that iterates over a queryset of Post objects named "posts_of_the_page". Each post is displayed in a Bootstrap card that shows the username of the author, the date and time when the post was created, and the content of the post. If the user is not anonymous, each card also includes a "Like" button that allows the user to like the post, and an "Edit" button that allows the user to edit their own posts.

The "Like" button is implemented as an ion-icon element that toggles its "active" class when clicked, and sends a fetch request to the server to update the number of likes.

The "Edit" button is implemented as a Bootstrap button that calls the "edit_post" JavaScript function when clicked. This function replaces the content of the post card with a textarea element, and adds a "Save" button and a "Cancel" button to the card footer. When the user clicks the "Save" button, the function sends a fetch request to the server to update the content of the post, and replaces the textarea with the updated content. If the user clicks the "Cancel" button, the function replaces the textarea with the original content.

profile.html:
This is a Django template for rendering a user's profile page. It extends a base layout template and defines a block for the page body. The body includes the user's follower and following counts, and a button to follow or unfollow the user depending on whether the profile belongs to the current user or not.

The template also includes a loop that iterates over the user's posts and renders them as cards. Each post card includes the post content, the user who posted it, the post date, the number of likes it has received, and an icon that the user can click to like or unlike the post. If the post was already liked by the current user, the icon is highlighted in red. If the post belongs to the current user, an edit button is displayed that allows the user to edit the post.

following.html:
This is a Django template for the "following" page of the social network web application. The page displays a list of posts made by users that the currently logged in user is following.

The template extends the base layout template "network/layout.html" and loads the static files required for the page. It contains two blocks: "scripts" and "body".

The "scripts" block includes a reference to the main JavaScript file for the application.

The "body" block displays a header with the text "Following" and a list of posts made by users that the currently logged in user is following. For each post, the template displays the username of the poster, the date and time the post was made, the post content, the number of likes the post has received, and an option to edit the post if the currently logged in user is the owner of the post.

The template uses Django template language syntax to generate dynamic content, such as iterating over a list of posts to display them on the page, generating URLs to link to user profiles, and checking if the currently logged in user has liked a post to display the appropriate heart icon.

main.js:
The code is a Django template file that displays a list of posts from the users that the current user is following. Each post is displayed in a card with its content, author, date, and the number of likes. The user can like a post by clicking on the heart icon and edit their own post by clicking on the edit button.

The JavaScript code in the template file contains two functions, like_post and edit_post.


The like_post function is called when the user clicks on the heart icon of a post. It toggles the active class of the heart icon and sends a fetch request to the server to update the like count of the post. When the fetch request is successful, the function updates the like count displayed on the page.

The edit_post function is called when the user clicks on the edit button of their own post. It replaces the post content with a textarea element, adds a save button and a cancel button to the card footer, and replaces the edit button with the save button. When the user clicks on the save button, the function sends a fetch request to the server to update the post content. If the fetch request is successful, the function updates the post content and date displayed on the page, and replaces the save button and the cancel button with the edit button.

The update_edit function is called by the edit_post function when the fetch request to update the post content is successful. It replaces the textarea element with a p element containing the new post content and updates the post date displayed on the page.

There is also a getCookie function that is called by the edit_post function to get the value of the CSRF token cookie.

view.py:
index view function: This view function handles the homepage of the application. It accepts GET and POST requests. When a user submits a new post via a POST request, it validates the form data, creates a new Post object and inserts it into the database. Then, it redirects the user to the homepage. If the request is a GET request, it retrieves all the posts from the database and renders the homepage template with the posts, a form to submit a new post and a list of liked posts for the current user.

profile view function: This view function handles the user profile page. It accepts a GET request with a user_id parameter to identify the user whose profile is being viewed. It retrieves all the posts by the user and renders the profile template with the posts, the user's follower and following count, and a list of liked posts for the current user.

following view function: This view function handles the page that displays all the posts of the users who the current user is following. It retrieves all the posts of the users who the current user is following and renders the following template with the posts and a list of liked posts for the current user.

like view function: This view function handles the functionality to add or remove a like from a post. It accepts a POST request with a postId parameter to identify the post that is being liked or unliked. If the current user has already liked the post, it removes the like. Otherwise, it adds the like. It returns a JSON response with the updated like count and whether the post was liked or unliked.

edit view function: This view function handles the functionality to edit a post. It accepts a POST request with a postId parameter to identify the post that is being edited. It retrieves the new content from the request body, updates the post in the database, and returns a JSON response with the updated content and date.

login_view view function: This view function handles the login page. It accepts a GET request to render the login template and a POST request to authenticate the user. If the user is authenticated successfully, it logs them in and redirects them to the homepage. Otherwise, it renders the login template with an error message.

logout_view view function: This view function handles the logout functionality. It logs out the user and redirects them to the homepage.

register view function: This view function handles the registration page. It accepts a GET request to render the registration template and a POST request to create a new user. It validates the form data, creates a new User object, and logs them in. If the form data is invalid or the username is already taken, it renders the registration template with an error message.
