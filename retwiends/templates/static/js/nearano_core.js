Core = function()           // Kedi s�n�f�n�n constructor'�.
{
    
    this.disconnect = dismaker;  // miyavla ad�nda bir method ekledik
}
function dismaker()           // bu fonksiyon asl�nda Kedi s�n�f�na ait
{
    alert('Benim ad�m ' + this.ad + '. Miyaaav');
}