import React from 'react'
import {useParams} from 'react-router-dom'
import Select from 'react-select'
import {useState} from 'react'
import {Link} from 'react-router-dom'
import { Dialog, DialogBackdrop, DialogPanel, DialogTitle } from '@headlessui/react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'
export default function 
() {
    const {id} = useParams()
    const [open, setOpen] = useState(false)

    // fetching and such here
    const [title, setTitle] = useState('')
    const [activity, setActivity] = useState('')
    const [area, setArea] = useState('')
    const [nature, setNature] = useState('')
    const [industry, setIndustry] = useState('')
    const [accommodation, setAccommodation] = useState('')
    const [link, setLink] = useState('')
        const handlePreview = () => {
            setOpen(true)
        }

        const handleSubmit = (e) => {
            e.preventDefault()
            console.log('hi')
        }

        const handleDelete = () => {
            //delete the current accommodation
        }

  return (
    <div className='w-4/5 mx-auto'>

        <div className='flex flex-row justify-between my-10'>
            <div className="flex flex-row">
                <div className='my-auto'>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="angle-left-solid">
<path id="Vector" d="M14.2734 3.21094L6.02344 11.4609L5.50781 12L6.02344 12.5391L14.2734 20.7891L15.3516 19.7109L7.64062 12L15.3516 4.28906L14.2734 3.21094Z" fill="black"/>
</g>
</svg>
</div>


    <div className='mx-10 text-4xl'>
        Knee Brace
    </div>
    </div>

        <div className='flex flex-row'>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="trash-alt">
<path id="Vector" d="M11.25 3C10.8574 3 10.4561 3.1377 10.1719 3.42188C9.8877 3.70605 9.75 4.10742 9.75 4.5V5.25H5.25V6.75H6V18.75C6 19.9834 7.0166 21 8.25 21H17.25C18.4834 21 19.5 19.9834 19.5 18.75V6.75H20.25V5.25H15.75V4.5C15.75 4.10742 15.6123 3.70605 15.3281 3.42188C15.0439 3.1377 14.6426 3 14.25 3H11.25ZM11.25 4.5H14.25V5.25H11.25V4.5ZM7.5 6.75H18V18.75C18 19.166 17.666 19.5 17.25 19.5H8.25C7.83398 19.5 7.5 19.166 7.5 18.75V6.75ZM9 9V17.25H10.5V9H9ZM12 9V17.25H13.5V9H12ZM15 9V17.25H16.5V9H15Z" fill="#D90000"/>
</g>
</svg>
        <p onClick={handleDelete} className='text-base ms-3 text-red-600'>
        Delete Accommodation
        </p>
        </div>
        </div>

        <div className="flex">
        <div className='w-1/2 flex flex-col'>
            <form onSubmit={handleSubmit} className="flex flex-col" >

            <div className='flex flex-row text-base text-gray-900 my-4'>The following content was generated with AI, please carefully verify its accuracy. </div>

                <label className='flex flex-col' >
                    <div className='flex flex-row text-base text-black'>Title <p className='text-red-600 ms-1'>*</p></div>
                    <input type="text"
                    onChange={(e)=>{setTitle(e.target.value)}} value={title}
                    className='border-2 rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400 mt-2' />

                </label>

                <label className='flex flex-col' >
                    <div className='flex flex-row text-base text-black'>Activity</div>
                    <input type="text" 
                    onChange={(e)=>{setActivity(e.target.value)}} value={activity}
                    className='border-2 rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400 mt-2' />

                </label>

                <label className='flex flex-col' >
                    <div className='flex flex-row text-base text-black'>Area of Body / Injury</div>
                    <Select options={[
        {value: 'natureOfInjury', label: 'Nature of Injury'},
        {value: 'accommodationName', label: 'Accommodation Name'}
    ]} className='mb-3 mt-2 border rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400' 
    onChange={(e) => setArea(e)}
    />
                </label>

                <label className='flex flex-col' >
                    <div className='flex flex-row text-base text-black'> Nature of Injury</div>
                    <Select options={[
        {value: 'natureOfInjury', label: 'Nature of Injury'},
        {value: 'accommodationName', label: 'Accommodation Name'}
    ]} className='mb-3 mt-2 border rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400 '
    onChange={(e)=>{setNature(e.target.value)}}
    />
                </label>

                <label className='flex flex-col' >
                    <div className='flex flex-row text-base text-black'> NAICS Industry</div>
                    <Select options={[
        {value: 'natureOfInjury', label: 'Nature of Injury'},
        {value: 'accommodationName', label: 'Accommodation Name'}
    ]} className='mb-3 mt-2 border rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400'
    onChange={(e)=>{setIndustry(e.target.value)}} 
    />
                </label>

                <label className='flex flex-col' >
                <div className='flex flex-row justify-between text-base text-black'>
                    <div className='flex flex-row'>
                    Description of Accommodation <p className='text-red-600 ms-1'>*</p>
                    </div>
                    <div className='text-gray-400'>
                    500 words max
                    </div>
                </div>
                <textarea 
                 onChange={(e)=>{setAccommodation(e.target.value)}} value={accommodation}
                required type="input fied" className='border-2 border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400 mt-2' />

                </label>
            
            </form>
            <div className='flex my-10 flex-row'>
            <button
            onClick={handleSubmit}
            className="flex w-2/4 mt-5 justify-center hover:bg-gray-800 rounded-3xl bg-sky-600 text-white px-3 py-3 me-1 text-sm font-semibold leading-6 shadow-sm
            ">
            Confirm Verification
          </button>
          <button
          onClick={handlePreview}
            className="flex w-1/3 mt-5 justify-center hover:border-gray-800 hover:text-white hover:bg-gray-800 rounded-3xl border-2 text-sky-600 border-sky-600 mx-1 px-3 py-3 text-sm font-semibold leading-6 shadow-sm">
            Preview Page
          </button>
          </div>
        </div>

        <div className='w-1/2'>
        <div className='justify-end flex'>
            <Link to={link} className='text-sky-600 flex'> <p className="underline mx-1 "> Open document in new window </p>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <g id="external-link-alt-solid">
            <path id="Vector" d="M13.5 3.75V5.25H17.6719L8.46094 14.4609L9.53906 15.5391L18.75 6.32812V10.5H20.25V3.75H13.5ZM3.75 6.75V20.25H17.25V10.5L15.75 12V18.75H5.25V8.25H12L13.5 6.75H3.75Z" fill="#0076BF" />
          </g>
        </svg>
            </Link>
            </div>
        </div>
        </div>
        <Dialog open={open} onClose={setOpen} className="relative z-10">
      <DialogBackdrop
        transition
        className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity data-[closed]:opacity-0 data-[enter]:duration-300 data-[leave]:duration-200 data-[enter]:ease-out data-[leave]:ease-in"
      />

      <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div className="flex min-h-full w-screen items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <DialogPanel
            transition
            className="relative transform w-full overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all data-[closed]:translate-y-4 data-[closed]:opacity-0 data-[enter]:duration-300 data-[leave]:duration-200 data-[enter]:ease-out data-[leave]:ease-in sm:my-8 sm:w-full sm:max-w-5xl data-[closed]:sm:translate-y-0 data-[closed]:sm:scale-95"
          >

            <div className="bg-gray-50 flex flex-row justify-between px-4 py-3 sm:px-6">
                <div className="p-10 w-full flex flex-row justify-between ">
                <div>
                    <p className="text-2xl">
                        Preview Accommodation Page
                    </p>
                    <p className="text-gray-500">This is how the current information would appear on the accommodation page.</p>
                </div>
              <button
                type="button"
                data-autofocus
                onClick={() => setOpen(false)}
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="close">
<path id="icon" d="M6.4 19L5 17.6L10.6 12L5 6.4L6.4 5L12 10.6L17.6 5L19 6.4L13.4 12L19 17.6L17.6 19L12 13.4L6.4 19Z" fill="#1D1B20"/>
</g>
</svg>

              </button>
              </div>
            </div>
            <div className="bg-white px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
            <p>hello world</p>
            </div>
          </DialogPanel>
        </div>
      </div>
    </Dialog>
        </div>

  )
}
