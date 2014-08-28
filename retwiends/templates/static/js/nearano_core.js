Core = function()           // Kedi sõnõfõnõn constructor'õ.
{
    
    this.disconnect = dismaker;  // miyavla adõnda bir method ekledik
}
function dismaker()           // bu fonksiyon aslõnda Kedi sõnõfõna ait
{
    alert('Benim adõm ' + this.ad + '. Miyaaav');
}