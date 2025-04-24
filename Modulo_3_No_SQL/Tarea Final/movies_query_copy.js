use Movies
// 1
db.movies.find()

// 2
db.movies.find().count()

// 3

var nuevaPelicula = {title: "Titanic", year: 1999, cast: ["David"], genres: ["Drama"]}

db.movies.insertOne(nuevaPelicula)

// 4

db.movies.deleteOne({title: "Titanic"})

// 5

db.movies.find({cast: "and"}).count()

// 6

var filtro = {cast: "and"};
var eliminar = {$pull: {cast: "and"}}

db.movies.updateMany(filtro, eliminar)

// 7

db.movies.find({"cast": {$size: 0}}).count()

// 8
var filtro2 = {"cast": {$size: 0}}
var actualizar = {$set: { "cast": ["Undefined"]}}

db.movies.updateMany(filtro2, actualizar)

// 9

db.movies.find({"genres": {$size: 0}}).count()

// 10
var filtro3 = {"genres": {$size: 0}}
var actualizar2 = { $set: {"genres": ["Undefined"]}}

db.movies.updateMany(filtro3, actualizar2)

db.movies.find({"genres": "Undefined"})

// 11
db.movies.find({}, {"year" : 1, "_id" : 0}).sort({"year": -1 }).limit(1)

// 12

var annoMaximo = db.movies.find({}, {year: 1, _id: 0}).sort({year: -1}).limit(1).toArray()[0].year;
var annoMinimo = annoMaximo - 20;

db.movies.aggregate([
  {
    $match: {
      year: {
        $gt: annoMinimo,
        $lte: annoMaximo
      }
    }
  },
  {
    $group: {
      _id: null,
      total: { $sum: 1 }
    }
  }
]);


// 13

db.movies.aggregate([
  {
    $match: {
      year: {
        $gte: 1960,
        $lte: 1969
      }
    }
  },
  {
    $group: {
      _id: null,
      total: { $sum: 1 }
    }
  }
]);

// 14

var maxPelis = db.movies.aggregate([
  {
    $group: {
      _id: "$year",            
      pelis: { $sum: 1 }       
    }
  },
  {
    $sort: { pelis: -1 }      // Contamos peliculas por año y ordenamos mayor a menor
  },
  {
    $group: {
      _id: "$pelis",           
      years: { $push: "$_id" } // Agrupamos por numero de películas en array con los años
    }
  },
  {
    $sort: { _id: -1 }        
  },
  {
    $limit: 1                 // Solo año con más películas
  },
  {
    $project: {
      _id: 0,                  
      pelis: "$_id",           
      years: 1                 // Mostrar los años con ese número de películas
    }
  }
]).toArray();

maxPelis;

// 15

var minPelis = db.movies.aggregate([
  {
    $group: {
      _id: "$year",            
      pelis: { $sum: 1 }       
    }
  },
  {
    $sort: { pelis: 1 }      // Contamos peliculas por año y ordenamos menor a mayor
  },
  {
    $group: {
      _id: "$pelis",           
      years: { $push: "$_id" } // Agrupamos por numero de películas en array con los años
    }
  },
  {
    $sort: { _id: 1 }        
  },
  {
    $limit: 1                 // Solo año con menos películas
  },
  {
    $project: {
      _id: 0,                  
      pelis: "$_id",           
      years: 1                 // Mostrar los años con ese número de películas
    }
  }
]).toArray();

minPelis;

// 16

db.movies.aggregate([
  {
    $unwind: "$cast"
  },
  {
    $project: {
      _id: 0
    }
  },
  {
    $out: "actors"
  }
]);

db.actors.find().count()



// 17

db.actors.aggregate([
  {
    $match: { cast: { $ne: "Undefined" } }  // Filtrar actores llamados "Undefined"
  },
  {
    $group: {
      _id: "$cast",
      cuenta: { $sum: 1 }
    }
  },
  {
    $sort: { cuenta: -1 }
  },
  {
    $limit: 5
  },
  {
    $project: {
      _id: 1,
      cuenta: 1
    }
  }
]);



// 18

db.actors.aggregate([
  {
    $group: {
      _id: {                   // Agrupar por película y año
        title: "$title",
        year: "$year"
      },
      actores: { $addToSet: "$cast" }  // Usamos $addToSet para asegurarnos de contar a cada actor solo una vez por película
    }
  },
  {
    $project: {
      _id: 1,                    // Mantener el título y el año
      cuenta: { $size: "$actores" }   // Contar el número de actores únicos en esa película y año
    }
  },
  {
    $sort: { cuenta: -1 }         // Ordenar por el número de actores de mayor a menor
  },
  {
    $limit: 5                     // Limitar a las 5 películas con más actores
  }
]);

// 19

db.actors.aggregate([
  {
    $match: { cast: { $ne: "Undefined" } } // 1. Filtramos "Undefined"
  },
  {
    $group: {
      _id: "$cast",              // 2. Agrupar por actor
      inicio: { $min: "$year" }, // Año más temprano
      fin: { $max: "$year" }     // Año más reciente
    }
  },
  {
    $project: {                  // 3. Calcular duración
      inicio: 1,
      fin: 1,
      duracion: { $subtract: ["$fin", "$inicio"] }
    }
  },
  {
    $sort: { duracion: -1 }      // 4. Ordenar por duración descendente
  },
  {
    $limit: 5                    // 5. Los 5 con carrera más larga
  }
]);

// 20

db.actors.aggregate([
  { $unwind: "$genres" },
  {
    $project: {
      _id: 0
    }
  },
  { $out: "genres" }
]);


db.genres.find().count(); // Contamos los documentos resultantes

// 21

db.genres.aggregate([
  {
    $match: {
      genres: { $ne: "Undefined" }  // Filtrar genres "Undefined"
    }
  },
  {
    $group: {
      _id: { year: "$year", genre: "$genres" },
      peliculas: { $addToSet: "$title" }  // Agrupar por año y género, contando títulos únicos
    }
  },
  {
    $project: {
      _id: 1,
      totalPeliculas: { $size: "$peliculas" }  // Contar películas distintas
    }
  },
  {
    $sort: { totalPeliculas: -1 }  // Ordenar de mayor a menor
  },
  {
    $limit: 5  // Solo los 5 con más películas
  }
]);

// 22

db.genres.aggregate([
  {
    $match: {
      cast: { $ne: "Undefined" },     // Excluir actores "Undefined"
      genres: { $ne: "Undefined" }    // Y también géneros "Undefined"
    }
  },
  {
    $group: {
      _id: "$cast",                   // Agrupar por actor
      generos: { $addToSet: "$genres" } // Recopilar géneros únicos
    }
  },
  {
    $project: {
      _id: 1,
      numgeneros: { $size: "$generos" }, // Contar número de géneros
      generos: 1
    }
  },
  {
    $sort: { numgeneros: -1 }         // Ordenar por número de géneros distintos
  },
  {
    $limit: 5                         // Obtener solo los 5 primeros
  }
]);

// 23

db.genres.aggregate([
  {
    $match: {
      genres: { $ne: "Undefined" } // Filtrar géneros no definidos
    }
  },
  {
    $group: {
      _id: { title: "$title", year: "$year" }, // Agrupar por título y año
      generos: { $addToSet: "$genres" }        // Agrupar géneros únicos
    }
  },
  {
    $project: {
      numgeneros: { $size: "$generos" },       // Calcular número de géneros únicos
      generos: 1
    }
  },
  {
    $sort: { numgeneros: -1 }                  // Ordenar por número de géneros descendente
  },
  {
    $limit: 5                                  // Tomar solo los 5 con más géneros
  }
]);




