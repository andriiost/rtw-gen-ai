import { React, useEffect, useState } from 'react'
import Trash from '../assets/trash.png'
import Select from 'react-select'

const SortingModal = ({ title, categoryOptions, subOptions }) => {
    const [numFilters, setNumFilters] = useState([1])
    useEffect(() => {
        console.log(numFilters)
    }, [numFilters])
    return (
        <div className='absolute mt-4 border-2 bg-white border-slate-500 shadow-[0_5px_20px_2px_rgba(0,0,0,0.2)] z-20 rounded-lg p-4 py-5 w-96'>
            {numFilters.map((filter, i) => {
                return (
                    <div key={i}>
                        {filter > 1 && (<div className='h-0.5 rounded-md bg-gray-200 mt-4 mb-4'/>)}
                        <div className='flex w-full justify-between items-center mb-3'>
                            <h3 className='text-lg font-bold'>{title + " " + filter}</h3>
                            <img className='w-3 h-3.5 mr-2' src={Trash}></img>
                        </div>
                        <p className='text-slate-500 text-sm mb-1'>Category</p>
                        <Select options={categoryOptions} className='mb-3' />
                        <p className='text-slate-500 text-sm mb-1'>{title + " By"}</p>
                        <Select options={subOptions} className='mb-3' />
                    </div>
                )
            })}
            <div className='flex items-center justify-between mt-8'>
                <p className='text-sky-600 hover:underline hover:cursor-pointer' 
                onClick={() => {setNumFilters([...numFilters, numFilters[numFilters.length-1] + 1])}}>+ Add filter</p>
                <button className='bg-sky-600 hover:bg-sky-900 p-3 px-8 rounded-3xl text-white'>
                    Apply
                </button>
            </div>
        </div>
    )
}

export default SortingModal