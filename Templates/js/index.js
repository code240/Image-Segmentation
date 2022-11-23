const pushback = (time) => {
    setTimeout(()=>{
        window.history.back()
    },time*1000)
}
const goto = (address,time) => {
    setTimeout(()=>{
        window.location.assign(address);
    },time*1000)
}