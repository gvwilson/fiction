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

const fixNotes = () => {
    Array.from(document.querySelectorAll('section')).forEach((section, i) => {
        // Only create list for footnotes at end of section if there are footnotes
        var list = undefined
        Array.from(section.querySelectorAll('span.note')).forEach((note, j) => {
	    // Create footnote list if not already done
            if (list === undefined) {
                list = document.createElement('ol')
                section.appendChild(list)
            }

            // Unique IDs forward and backward
            const note_label = `note-${i+1}-${j+1}`
            const anchor_label = `anchor-${i+1}-${j+1}`

            // Insert forward-linked footnote
            const forward = document.createElement('a')
            forward.setAttribute('href', `#${note_label}`)
            forward.setAttribute('id', anchor_label)
            forward.textContent = `${j+1}`
            const marker = document.createElement('sup')
            marker.appendChild(forward)
            note.parentNode.insertBefore(marker, note)

            // Move footnote text and add backward link
            const li = document.createElement('li')
            li.setAttribute('id', note_label)
            list.appendChild(li)
            li.appendChild(note)
            note.classList.remove('note')
            const backward = document.createElement('a')
            backward.setAttribute('href', `#${anchor_label}`)
            backward.textContent = `\u2934`
            li.appendChild(backward)
        })
    })
}

const fixPage = () => {
    fixToc()
    fixNotes()
}
