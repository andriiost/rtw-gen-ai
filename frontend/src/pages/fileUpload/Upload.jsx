import React from 'react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Loading from '../../components/Loading'
import Error from '../../components/Error'
export default function Upload() {
    const [file, setFile] = useState(null)
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()
    const uploadFile = async (e) => {
        e.preventDefault()
        //upload file
        try{
            setLoading(true)
            setError(null)
            //req

            setLoading(false)
        }catch(err){
            setError(err)
            setLoading(false)
        }
        //display fetched info?

        //navigate
    }

  return (
    <div>
    Upload
    <label>
    <input type="file" />
    </label>
    </div>
  )
}
