import {withRouter} from 'react-router-dom';

class LoginCheck extends React.component {

    constructor(props){

    }

    componentDidMount(){
        this.props.history.push('/login');
    }

}

export default withRouter(Component);