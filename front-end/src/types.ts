export interface IFormData {
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

export const exampleData: IFormData = {
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
}

export interface IResponseData {
  id: string,
  state: string,
  results: IResultData
}

export interface IResultData {
  prediction: number,
  predict_proba: {
    "0": number,
    "1": number
  }
}