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
        } else {
            link.classList.add("display-none")
        }
    }
    for (var tooltip of document.getElementsByClassName("tooltip")){
        if (tooltip.classList.contains("display-none")){
            tooltip.classList.remove("display-none")
        } else {
            tooltip.classList.add("display-none")
        }
    }
    // var last = JSON.parse(sessionStorage.getItem("sidebarCollapsed"))
    // if (last == null){
    //     last = false
    // }
    // if (last)
    // sessionStorage.setItem("sidebarCollapsed", last)
    // console.log(sessionStorage.getItem("sidebarCollapsed"))
}

// var last = sessionStorage.getItem("sidebarCollapsed")
// if (last == null){
//     last = false
// }
// console.log(last)
// if (last){
//     toggleSidebar()
// }