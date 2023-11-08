import React, { useState, ChangeEvent, FormEvent } from 'react'
import axios from 'axios'

// Define the shape of your form data
interface IFormData {
  age: number
  sex: number
  cp: number
  trestbps: number
  chol: number
  fbs: number
  restecg: number
  thalach: number
  exang: number
  oldpeak: number
  slope: number
  ca: number
  thal: number
}

function App() {
  const [formData, setFormData] = useState<IFormData>({
    age: 85,
    sex: 1,
    cp: 3,
    trestbps: 120,
    chol: 233,
    fbs: 1,
    restecg: 0,
    thalach: 150,
    exang: 0,
    oldpeak: 2.3,
    slope: 1,
    ca: 0,
    thal: 3,
  })

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) })
  }

  const local_url = 'http://localhost:8000/predict'

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    try {
      const response = await axios.post(local_url, formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      console.log(response.data)
      // Handle the response from the server here
    } catch (error) {
      console.error('There was an error!', error)
    }
  }

  return (
    <div className='App'>
      <form onSubmit={handleSubmit}>
        {/* Render your form fields based on formData */}
        {Object.entries(formData).map(([key, value]) => (
          <input
            key={key}
            type='number'
            name={key}
            value={value}
            onChange={handleChange}
          />
        ))}
        <button type='submit'>Predict</button>
      </form>
    </div>
  )
}

export default App
