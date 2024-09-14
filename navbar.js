$(".menu > ul > li").click(function (e){
    // Removes from other tabs
    $(this).siblings().removeClass("active");
    // Adds class to clicked tab
    $(this).toggleClass("active");
    // Show subpages if applicable
    $(this).find("ul").slideToggle();
    // Close other subpages if open
    $(this).siblings().find("ul").slideUp();
});

$(".menu-btn").click(function() {
    $(".container").toggleClass("active")
    $(".overlay").toggleClass("Active")
})