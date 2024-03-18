export default function SignUp() {
    const initialFormData = Object.freeze({
        email: '',
        phone_number:'',
        password: '', 
    });

    const [formData ,updateFormData] = useState(initialFormData);

    const handleChange = (e) => {
        updateFormData({
            ...formData,
            // Trimming any whitespace
            [e.target.name]: e.target.value.trim(),

        });
    };
}