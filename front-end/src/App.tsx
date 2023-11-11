import React, { useState, ChangeEvent, FormEvent } from 'react'
import axios, { AxiosResponse } from 'axios'

import { IFormData, IResponseData, IResultData, exampleData } from './types'

function App() {
  const [responseData, setResponseData] = useState<IResponseData | null>(null)
  const [formData, setFormData] = useState<IFormData>(exampleData)

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) })
  }

  const baseApiURL = process.env.REACT_APP_API_URL
  const predictionEndpoint = new URL('/prediction', baseApiURL).toString()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    let response: AxiosResponse<IResponseData> | undefined
    try {
      response = await axios.post(predictionEndpoint, formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
    } catch (error) {
      console.error('There was an error!', error)
      return
    }

    if (!response) {
      console.error('There was no response data!')
      return
    }

    const { data } = response
    setResponseData(data)
    console.log('Request ID', data.id)
  }

  const handleCheckResponse = async () => {
    if (!responseData) {
      return
    }

    const predictionResultsEndpoint = new URL(`/prediction/${responseData.id}`, baseApiURL).toString()
    let response: AxiosResponse<IResponseData> | undefined
    try {
      response = await axios.get(predictionResultsEndpoint, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
    } catch (error) {
      console.error('There was an error!', error)
      return
    }

    if (!response) {
      return
    }

    const { data } = response
    setResponseData(data)
    if (!data.results) {
      console.log('Nothing so far')
      return
    }
  }

  const handleReset = () => {
    setFormData(exampleData)
    setResponseData(null)
  }


  let atRiskForHeartDisease: boolean = false
  let probabilityOfResult: number = 0
  const resultsCompleted = responseData?.state === 'COMPLETED'
  if (responseData?.results) {
    atRiskForHeartDisease = responseData?.results.prediction === 1
    probabilityOfResult = (atRiskForHeartDisease ? responseData?.results.predict_proba["1"] : responseData?.results.predict_proba["0"]) ?? 0
  }


  return (
    <div className='App'>
      <form onSubmit={handleSubmit}>
        {Object.entries(formData).map(([key, value]) => (
          <div>
            <span>{key}</span>
            <input
              key={key}
              type='number'
              name={key}
              value={value}
              onChange={handleChange}
            />
          </div>
        ))}
        <button type='submit'>1. Start Prediction Request</button>
      </form>
      <div>
        <button type='button' onClick={handleCheckResponse}>2. Check Status of Request</button>
      </div>
      <div>
        <button type='button' onClick={handleReset}>3. Reset</button>
      </div>
      {!resultsCompleted && responseData && (
        <div>
          <p>Results are still being processed...</p>
          <p>Use "Check Status of Request" to see if the results have been updated.</p>
        </div>
      )}
      {resultsCompleted && (
        <div>
          <h2>Status</h2>
          <div>{responseData.state}</div>
          <h2>Result</h2>
          <p>{atRiskForHeartDisease ? 'These results indicate a risk of Heart Disease' : 'These results indicate no risk of Heart Disease'}</p>
          <p>There is a {Math.round(probabilityOfResult * 100)}% probability of this result.</p>
        </div>
      )}

    </div>
  )
}

export default App
