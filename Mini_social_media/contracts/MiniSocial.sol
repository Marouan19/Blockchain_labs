// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MiniSocial {
    // Structure to represent a comment
    struct Comment {
        string content;
        address author;
        uint256 timestamp;
    }

    // Structure to represent a post
    struct Post {
        uint256 postId;
        string title;
        string content;
        address author;
        uint256 timestamp;
        uint256 likesCount;
        address[] likedBy;
        mapping(uint256 => Comment) comments;
        uint256 commentCount;
        bool isEdited;
        uint256 lastEditTime;
        bool isActive;
    }

    // Array to store all posts
    Post[] private posts;

    // Mapping to track user likes on posts
    mapping(uint256 => mapping(address => bool)) private postLikes;
    
    // Total post count
    uint256 public totalPosts;
    uint256 public activePostsCount;

    // Events
    event PostCreated(uint256 indexed postId, address indexed author, string title, uint256 timestamp);
    event PostLiked(uint256 indexed postId, address indexed liker);
    event PostUnliked(uint256 indexed postId, address indexed unliker);
    event CommentAdded(uint256 indexed postId, uint256 indexed commentIndex, address indexed commenter, string content);

    // Modifier to check if post exists
    modifier postExists(uint256 _postId) {
        require(_postId < posts.length, "Post does not exist");
        require(posts[_postId].isActive, "Post has been deleted");
        _;
    }

    // Function to create a post
    function createPost(
        string memory _title,
        string memory _content
    ) public returns (uint256) {
        // Validations
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(bytes(_title).length <= 100, "Title too long");
        require(bytes(_content).length > 0, "Content cannot be empty");
        require(bytes(_content).length <= 5000, "Content too long");

        // Create the new post
        uint256 newPostId = totalPosts;
        Post storage newPost = posts.push();
        newPost.postId = newPostId;
        newPost.title = _title;
        newPost.content = _content;
        newPost.author = msg.sender;
        newPost.timestamp = block.timestamp;
        newPost.likesCount = 0;
        newPost.commentCount = 0;
        newPost.isEdited = false;
        newPost.lastEditTime = block.timestamp;
        newPost.isActive = true;
        
        totalPosts++;
        activePostsCount++;
        
        emit PostCreated(newPostId, msg.sender, _title, block.timestamp);
        
        return newPostId;
    }

    // Function to add a comment
    function addComment(uint256 _postId, string memory _content) public postExists(_postId) {
        require(bytes(_content).length > 0, "Le commentaire ne peut pas etre vide");
        require(bytes(_content).length <= 280, "Le commentaire est trop long");

        Post storage post = posts[_postId];
        uint256 commentIndex = post.commentCount;
        post.comments[commentIndex] = Comment({
            content: _content,
            author: msg.sender,
            timestamp: block.timestamp
        });
        post.commentCount++;
        
        emit CommentAdded(_postId, commentIndex, msg.sender, _content);
    }

    // Function to toggle like/unlike a post
    function toggleLike(uint256 _postId) public postExists(_postId) {
        require(msg.sender != posts[_postId].author, "Vous ne pouvez pas liker votre propre post");
        
        if (!postLikes[_postId][msg.sender]) {
            postLikes[_postId][msg.sender] = true;
            posts[_postId].likesCount++;
            posts[_postId].likedBy.push(msg.sender);
            emit PostLiked(_postId, msg.sender);
        } else {
            postLikes[_postId][msg.sender] = false;
            posts[_postId].likesCount--;

            for (uint i = 0; i < posts[_postId].likedBy.length; i++) {
                if (posts[_postId].likedBy[i] == msg.sender) {
                    posts[_postId].likedBy[i] = posts[_postId].likedBy[posts[_postId].likedBy.length - 1];
                    posts[_postId].likedBy.pop();
                    break;
                }
            }
            
            emit PostUnliked(_postId, msg.sender);
        }
    }

    // Function to get details of a post
    function getPost(uint256 _postId) public view postExists(_postId) returns (
        string memory title,
        string memory content,
        address author,
        uint256 timestamp,
        uint256 likesCount,
        address[] memory likedBy,
        uint256 commentCount,
        Comment[] memory comments
    ) {
        Post storage post = posts[_postId];
        Comment[] memory commentsArr = new Comment[](post.commentCount);
        uint256 commentIndex = 0;
        for (uint256 i = 0; i < post.commentCount; i++) {
            commentsArr[commentIndex++] = post.comments[i];
        }
        return (
            post.title,
            post.content,
            post.author,
            post.timestamp,
            post.likesCount,
            post.likedBy,
            post.commentCount,
            commentsArr
        );
    }

    // Function to get all active posts
    function getAllPosts() public view returns (
        uint256[] memory postIds,
        string[] memory titles,
        string[] memory contents,
        address[] memory authors,
        uint256[] memory timestamps,
        uint256[] memory likeCounts,
        uint256[] memory commentCounts,
        bool[] memory isEdited,
        bool[] memory isActive
    ) {
        uint256 activePostCount = 0;
        
        for (uint256 i = 0; i < posts.length; i++) {
            if (posts[i].isActive) {
                activePostCount++;
            }
        }
        
        postIds = new uint256[](activePostCount);
        titles = new string[](activePostCount);
        contents = new string[](activePostCount);
        authors = new address[](activePostCount);
        timestamps = new uint256[](activePostCount);
        likeCounts = new uint256[](activePostCount);
        commentCounts = new uint256[](activePostCount);
        isEdited = new bool[](activePostCount);
        isActive = new bool[](activePostCount);
        
        uint256 currentIndex = 0;
        
        for (uint256 i = 0; i < posts.length; i++) {
            if (posts[i].isActive) {
                postIds[currentIndex] = posts[i].postId;
                titles[currentIndex] = posts[i].title;
                contents[currentIndex] = posts[i].content;
                authors[currentIndex] = posts[i].author;
                timestamps[currentIndex] = posts[i].timestamp;
                likeCounts[currentIndex] = posts[i].likesCount;
                commentCounts[currentIndex] = posts[i].commentCount;
                isEdited[currentIndex] = posts[i].isEdited;
                isActive[currentIndex] = posts[i].isActive;
                currentIndex++;
            }
        }
        
        return (
            postIds,
            titles,
            contents,
            authors,
            timestamps,
            likeCounts,
            commentCounts,
            isEdited,
            isActive
        );
    }

    // Function to get the total count of active posts
    function getTotalPosts() public view returns (uint256) {
        return activePostsCount;
    }

    // Function to check if a user has liked a post
    function hasLiked(uint256 _postId, address _user) public view postExists(_postId) returns (bool) {
        return postLikes[_postId][_user];
    }

    // Function to delete a post (only the author)
    function deletePost(uint256 _postId) public postExists(_postId) {
        require(msg.sender == posts[_postId].author, "Seul l'auteur peut supprimer ce post");
        posts[_postId].isActive = false;
        activePostsCount--;
    }
    // Function to edit a post (only the author)
function editPost(uint256 _postId, string memory _newTitle, string memory _newContent) public postExists(_postId) {
    require(msg.sender == posts[_postId].author, "Only the author can edit this post");
    require(bytes(_newTitle).length > 0, "Title cannot be empty");
    require(bytes(_newContent).length > 0, "Content cannot be empty");
    require(bytes(_newTitle).length <= 100, "Title too long");
    require(bytes(_newContent).length <= 5000, "Content too long");

    Post storage post = posts[_postId];
    post.title = _newTitle;
    post.content = _newContent;
    post.isEdited = true;
    post.lastEditTime = block.timestamp;
}

}