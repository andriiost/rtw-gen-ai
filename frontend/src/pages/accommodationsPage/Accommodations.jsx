import { React, useState, useEffect } from 'react'
import accommodationsMock from '../../mockData/accommodationsMocks.json'
import CardView from './cardView/CardView'
import { ListView } from './listView/ListView'
import Card from './cardView/Card'
// import { ListView } from './listView/listView'
export const Accommodations = () => {
    const [data, setData] = useState([])
    const [view, setView] = useState(true)
    useEffect(() => {
        setData(accommodationsMock.accommodations);
        console.log(data)
    }, [data])
    console.log(data)
    return (
        <main className='p-6'>
            <h1 className='text-4xl'>List of Accommodations</h1>
            <section className='flex'>
                <div>
                    <input type='text' placeholder='Search'
                        className='border-neutral-300 border-2 rounded-sm p-1 w-full'/>
                </div>
                <div>
                    <button>

                    </button>
                </div>
            </section>
            <form className='grid grid-cols-6'>
                {/* menu at top */}
            </form>
            <section className='pt-6 pb-6'>
            {view ?
                <CardView cards={data} />
                :
                <p>bye</p>
            }
            </section>
        </main>
    )
}

// {view ? (<CardView cardsData={data} />) : <ListView listData={data} />}
