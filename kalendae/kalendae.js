// Requisiti del linguaggio di programmazione:
// disponibilita` di un classe "data" che rappresenti la data con anno, mese, e
// giorno.

// "Enumerativo" per il giorno della settimana.
// Questa corrispondenza deve essere stabilita secondo quanto definito nella
// documentazione della classe "data" disponibile.
var dow_enum = {"su":0, "mo": 1, "tu": 2, "we": 3, "th": 4, "fr": 5, "sa": 6};

var seven_day_indexes = [dow_enum.su, dow_enum.mo, dow_enum.tu,
dow_enum.we, dow_enum.th, dow_enum.fr, dow_enum.sa];

// "Enumerativo" per il mese dell'anno.
// Questa corrispondenza deve essere stabilita secondo quanto definito nella
// documentazione della classe "data" disponibile.
var month_enum = {"jan":0, "feb": 1, "mar": 2, "apr": 3, "may": 4, "jun": 5, "jul": 6, "aug": 7, "sep": 8, "oct": 9, "nov": 10, "dec": 11};

// Rotazione di un array.
// var a = [0,1,2,3,4,5,6]
// a.rotate(-1);
// adesso a vale 6,0,1,2,3,4,5
// http://stackoverflow.com/a/1985471/15485
Array.prototype.rotate = (function() {
    var unshift = Array.prototype.unshift,
        splice = Array.prototype.splice;

    return function(count) {
        var len = this.length >>> 0,
            count = count >> 0;

        unshift.apply(this, splice.call(this, count % len, len));
        return this;
    };
})();

// Copia deep di un array.
function deep_copy(a)
{
  var r = new Array;
  for ( var i = 0; i < a.length; i++ ) {
    r.push(a[i]);
  }
  return r;
}

// Restituisce l'oggetto Date corrispondente al giorno dopo la data d
// d e` un oggetto Date.
function next_day(d)
{
  d.setDate(d.getDate()+1);
  return d;
}

// Restituisce l'oggetto Date corrispondente al giorno prima la data d
// d e` un oggetto Date.
function prev_day(d)
{
  d.setDate(d.getDate()-1);
  return d;
}

// Restituisce il numero di settimana all'interno del mese della data d.
// d e` un oggetto Date.
// Il primo giorno del mese corrisponde alla settimana numero 1 di quel mese.
// La settimana inizia il giorno start_of_week.
function get_week(d,start_of_week)
{
  var current_date = new Date(d.getFullYear(),d.getMonth(),1,d.getHours(),d.getMinutes(),d.getSeconds(),d.getMilliseconds());
  var week_number = 1;
  if ( current_date.getTime() == d.getTime() ) return week_number;
  do{
    current_date = next_day(current_date);
    if ( current_date.getDay() == start_of_week ) {
      week_number++;
    }
  } while( current_date.getTime() != d.getTime() )
  return week_number;
}

// Restituisce le coordinate dei giorni del mese month dell'anno year.
// La settimana inizia il giorno start_of_week.
// Le coordinate sono l'indice di riga e di colonna per una rappresentazione
// come la seguente:
//
//     October 2016
// Su Mo Tu We Th Fr Sa
//                    1
//  2  3  4  5  6  7  8
//  9 10 11 12 13 14 15
// 16 17 18 19 20 21 22
// 23 24 25 26 27 28 29
// 30 31
//
// Gli indici sono zero-based quindi nell'esempio qui sopra il giorno 4 ottobre
// ha indice di riga uguale a 1 ed indice di colonna uguale a 2.
//
// Il valore ritornato da questa funzione e` un array di oggetti; ogni oggetto
// ha il campo "d" che e` un oggetto Date, il campo "row" che e` l'indice di 
// riga ed il campo "col" che e` l'indice di colonna.
function get_month_coord_week_on_row_day_on_col(year,month,start_of_week)
{
  return get_month_coord(year,month,start_of_week,"week_on_row_day_on_col");
}

function get_month_coord_day_on_row_week_on_col(year,month,start_of_week)
{
  return get_month_coord(year,month,start_of_week,"day_on_row_week_on_col");
}

function get_month_coord(year,month,start_of_week,type)
{
  var M = new Array;
  var d = new Date(year, month, 1);
  var offset = deep_copy(seven_day_indexes);
  offset.rotate(-start_of_week);
  do {
    if ( type == "day_on_row_week_on_col" ) {
      M.push({"d":new Date(d),"col":get_week(d,start_of_week)-1,"row":offset[d.getDay()]});
    } else if ( type == "week_on_row_day_on_col" ) {
      M.push({"d":new Date(d),"row":get_week(d,start_of_week)-1,"col":offset[d.getDay()]});
    }
    d = next_day(d);
  } while( d.getMonth() == month )
  return M;
}
