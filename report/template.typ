// Sets up the document, 
#let project(title: "", subtitle: "", authors: (), date: none, body) = {
  // Set the document's basic properties.
  set document(author: authors.map(a => a.name), title: title)
  set page(numbering: "1", number-align: center, margin: 2cm)

  // Set font family and sizes
  set text(font: "Roboto", lang: "en")
  set heading(numbering: "1.1")
  show heading: set text(weight: "light")


  // Title row.
  align(left)[
    #block(text(weight: "thin", 2.5em, title))
    #block(text(weight: "light", 1.2em, subtitle))
    #v(1em, weak: true)
    #date
  ]

  // Author information.
  authors.map(author => align(left)[#author.name - #author.email]).join()
  // pad(
  //   top: 0.5em,
  //   bottom: 0.5em,
  //   grid(
  //     columns: (1fr,) * calc.min(3, authors.len()),
  //     gutter: 1em,
  //     ..authors.map(author => align(left)[
  //       #author.name - #author.email
  //     ]),
  //   ),
  // )

  // Main body.
  set par(justify: true)

  body
}