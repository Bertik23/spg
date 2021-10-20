function toggleSidebar(){
    for (var brand of document.getElementsByClassName("brand")){
        if (brand.classList.contains("display-none")){
            brand.classList.remove("display-none")
        } else {
            brand.classList.add("display-none")
        }
    }
    for (var link of document.getElementsByClassName("text")){
        if (link.classList.contains("display-none")){
            link.classList.remove("display-none")
            link.parentElement.classList.remove("text-center")
        } else {
            link.classList.add("display-none")
            link.parentElement.classList.add("text-center")
        }
    }
    for (var tooltip of document.getElementsByClassName("tooltip")){
        if (tooltip.classList.contains("display-none")){
            tooltip.classList.remove("display-none")
        } else {
            tooltip.classList.add("display-none")
        }
    }
    for (var text of document.getElementsByClassName("cardText")){
        if (text.classList.contains("display-none")){
            text.classList.remove("display-none")
            text.parentElement.classList.remove("col-gap0")
            text.parentElement.classList.add("col-gap02rem")
        } else {
            text.classList.add("display-none")
            text.parentElement.classList.add("col-gap0")
            text.parentElement.classList.remove("col-gap02rem")
        }
    }
    var last = JSON.parse(sessionStorage.getItem("sidebarCollapsed"))
    if (last == null){
        last = false
    }
    if (last)
    sessionStorage.setItem("sidebarCollapsed", last)
    console.log(sessionStorage.getItem("sidebarCollapsed"))
}

var last = sessionStorage.getItem("sidebarCollapsed")
if (last == null){
    last = false
}
console.log(last)
if (last){
    toggleSidebar()
}