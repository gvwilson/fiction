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
    // Collect all footnotes.
    const originalFootnotesDiv = document.querySelector('div.footnotes')
    const footnotes = new Map()
    Array.from(document.querySelectorAll('[role="doc-endnote"]')).forEach(note => {
	footnotes.set(note.getAttribute('id'), note)
    })

    // Move to section.
    Array.from(document.querySelectorAll('section')).forEach((section, sectionNum) => {
	// Skip if no footnotes in section.
	const refs = Array.from(section.querySelectorAll('a.footnote'))
	if (refs.length > 0) {
	    // Create a home.
	    const div = document.createElement('div')
	    div.classList.add('footnotes')
	    section.appendChild(div)
	    const ol = document.createElement('ol')
	    ol.setAttribute('id', `footnote-list-${sectionNum}`)
	    div.appendChild(ol)

	    // Move elements, recording IDs.
	    refs.forEach(r => {
		const id = r.getAttribute('href').substring(1)
		const target = footnotes.get(id)
		target.parentNode.removeChild(target)
		ol.appendChild(target)
	    })

	    // Start numbering list at the right value.
	    const refIds = refs.map(r => r.textContent)
	    ol.setAttribute('start', refIds[0])
	}
    })

    // Clean up.
    originalFootnotesDiv.parentNode.removeChild(originalFootnotesDiv)
}

const fixPage = () => {
    fixToc()
    fixFootnotes()
}
