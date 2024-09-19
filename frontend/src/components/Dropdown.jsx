import { React, useState } from 'react'
import SortingModal from './SortingModal'
import DownArrow from '../assets/downArrow.png'

const Dropdown = ({ icon, title, categoryOptions, subOptions }) => {
    const [open, setOpen] = useState(false)
    return (
        <div className='border-2 w-fit rounded-md border-slate-400 hover:bg-neutral-100 justify-between transition ease-in hover:ease-out' onClick={() => setOpen(true) }>
            <div className='flex items-center'>
                <img src={icon} alt='sortingIcon' className='pl-2' />
                <h2 className='font-semibold text-slate-500 p-2'>{title}</h2>
                <img src={DownArrow} alt='downArrow' className='pr-3' />
            </div>
            {open && (
                <div>
                    <div className='fixed w-screen h-screen top-0 left-0 z-10' onClick={(e) => {e.stopPropagation(); setOpen(false)}}/>
                    <SortingModal title={title}
                        categoryOptions={categoryOptions}
                        subOptions={subOptions} />
                </div>
            )}
        </div>
    )
}

export default Dropdown