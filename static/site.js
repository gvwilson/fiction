const fixToc = () => {
    const toc = document.querySelector('ol#toc')
    if (! toc) {
	return
    }
    Array.from(document.querySelectorAll('h2')).forEach((header, i) => {
	const label = `chapter.${i+1}`
	header.id = label
	const text = header.innerHTML
	const item = document.createElement('li')
	item.innerHTML = `<a href="#${label}">${text}</a>`
	toc.appendChild(item)
    })
}

const fixFootnotes = () => {
    Array.from(document.querySelectorAll('section')).forEach((section, i) => {
	const list = document.createElement('ol')
	Array.from(section.querySelectorAll('sup')).forEach((sup, j) => {
	    backref = `backref.${i+1}.${j+1}`
	    footnote = `footnote.${i+1}.${j+1}`
	    const text = sup.innerHTML
	    sup.id = backref
	    sup.innerHTML = `<a href="#${footnote}">${j+1}</a>`
	    const item = document.createElement('li')
	    item.id = footnote
	    item.innerHTML = `${text} <a href="#${backref}">&#x21F1;</a>`
	    list.appendChild(item)
	})
	if (list.childElementCount > 0) {
	    section.appendChild(list)
	}
    })
}

const fixSidenotes = (onSide) => {
    Array.from(document.querySelectorAll('section')).forEach((section, i) => {
	// Side notes
	if (onSide) {
	    Array.from(section.querySelectorAll('span.sidenote')).forEach((span, j) => {
		const counter = document.createElement("span")
		counter.textContent = `${j+1}) `
		span.insertBefore(counter, span.firstChild)
		const marker = document.createElement("sup")
		marker.textContent = `${j+1}`
		span.parentNode.insertBefore(marker, span)
	    })
	}
	// Bottom notes
	else {
	    const list = document.createElement("ol")
	    section.appendChild(list)
	    Array.from(section.querySelectorAll('span.sidenote')).forEach((span, j) => {
		const marker = document.createElement("sup")
		marker.textContent = `${j+1}`
		span.parentNode.insertBefore(marker, span)
		span.classList.remove("sidenote")
		const li = document.createElement("li")
		list.appendChild(li)
		li.appendChild(span)
	    })
	}
    })
}

const getNotesOnSide = () => {
    const meta_value = document.querySelector("meta[name='sidenotes']")
    return meta_value && (meta_value.getAttribute("content") == "true")
}

const fixPage = () => {
    const onSide = getNotesOnSide()
    fixToc()
    fixFootnotes()
    fixSidenotes(onSide)
}
