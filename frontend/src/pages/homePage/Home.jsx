import React from 'react'
import NavBar from '../../components/NavBar'
import Footer from '../../components/Footer'
import axios from 'axios'

export default function Home() {
    const test = async () => {
        const res = await axios.get('http://127.0.0.1:8080/');
        console.log(res.data);
    }
    return (
        <>
          
            <div className="h-96">        
                <h1>I AM THE HOMEPAGE HEHEEHHA</h1>
                <button onClick={() => test()}>
                    CLICK ME PSL
                </button>
            </div>
            
        </>
    )
}
