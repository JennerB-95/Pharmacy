const getUrlParameter = () => {
  const url = location.href.split('/')
  return Number(url[url.length - 2])
}

const buildRequestData = className => {
  const data = {}
  for (const field of document.getElementsByClassName(className)) 
    data[field.name]  = field.value
  return data
}

const getTodayDate = () => {
  const today = new Date()
  return today.getFullYear() + '-' + today.getMonth() + 1 + '-'  + today.getDate()
}

const buildRequestFormData = className => {
  const data = new FormData()
  for (const field of document.getElementsByClassName(className)) {
    if (field.type == 'file' && $(field)[0].files[0])
      data.append(field.name, $(field)[0].files[0])
    else if (field.type != 'file' && field.name != 'birthdate')
      data.append(field.name, field.value)
    if (field.name == 'birthdate')
      data.append(field.name, moment(field.value, 'DD/MM/YYYY').format('YYYY-MM-DD'))
    if (field.name == 'comission') 
      data.append(field.name, Number(field.value).toFixed(2) / 100)
    if (field.name == 'password')
      data.append('raw_password', field.value)
  }
  return data
}

const buildQueryParams = className => {
  let queryParams = '?'
  for (const field of document.getElementsByClassName(className)) {
    queryParams += `${field.name}=${field.value}&`
  }
  return queryParams
}

const formatCurrency = number => {
    let formatted = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'EUR'}).format(number)
    formatted = formatted.split('')
    formatted[0] = 'Q'
    console.log(number);
    return formatted.join('')
}
