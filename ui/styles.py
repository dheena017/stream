def get_css():
    return """
    <style>
    .chat-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .chat-status-container {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    .status-badge {
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        background-color: #d1fae5;
        color: #065f46;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .main-header {
        margin: 0;
        font-size: 1.5rem;
        color: #1f2937;
    }
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .chat-header-container {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
        .main-header {
            font-size: 1.2rem;
        }
        .chat-status-container {
            width: 100%;
            justify-content: flex-start;
        }
    }
    </style>
    """
