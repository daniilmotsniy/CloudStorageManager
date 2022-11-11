import API from './API';

const API_HOST = '127.0.0.1:8000';
const API_PROTOCOL = 'http:';
const API_URL = `${API_PROTOCOL}//${API_HOST}`;


const api = new API(API_URL);
api.setUp();
export {
    api,
};