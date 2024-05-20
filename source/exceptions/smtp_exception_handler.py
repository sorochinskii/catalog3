from smtplib import SMTPRecipientsRefused

SMTP_ERROR_CODES = {
    211: "System status, or system help reply.",
    214: "Help message.",
    220: "Service ready.",
    221: "Service closing transmission channel.",
    235: "Authentication successful.",
    250: "Requested mail action okay, completed.",
    251: "User not local; will forward to {}",
    252: "Cannot VRFY user, but will accept message and attempt delivery.",
    354: "Start mail input; end with <CRLF>.<CRLF>",
    421: "Service not available, closing transmission channel. The server response was: {}",
    450: "Requested mail action not taken: mailbox unavailable. The server response was: {}",
    451: "Requested action aborted: local error in processing.",
    452: "Requested action not taken: insufficient system storage.",
    455: "Server unable to accommodate parameters.",
    500: "Syntax error, command unrecognized.",
    501: "Syntax error in parameters or arguments.",
    502: "Command not implemented.",
    503: "Bad sequence of commands.",
    504: "Command parameter not implemented.",
    530: "Authentication required.",
    534: "Authentication mechanism is too weak.",
    535: "Authentication failed. The server response was: {}",
    538: "Encryption required for requested authentication mechanism.",
    550: "Requested action not taken: mailbox unavailable. The server response was: {}",
    551: "User not local; please try {}. The server response was: {}",
    552: "Requested mail action aborted: exceeded storage allocation.",
    553: "Requested action not taken: mailbox name not allowed.",
    554: "Transaction failed. The server response was: {}",
}


class SmtpErrorHandler:

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_instance, traceback):
        match(type(ex_instance)):
            case SMTPRecipientsRefused:
                ...
